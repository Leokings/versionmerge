import json


POLICY = "Classify semantic changes section by section and mark incompatible simultaneous changes as conflicts."
BASE = ["Access is available on weekdays only.", "Reports are published every month."]


def _open(contract, vm, owner, left_author, right_author, left, right, key="policy"):
    vm.sender = owner
    return contract.open_merge(key, left_author, right_author, json.dumps(BASE), json.dumps(left), json.dumps(right), POLICY)


def test_independent_changes_auto_merge_by_section(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    right = [BASE[0], "Reports are published every two weeks."]
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, right)
    direct_vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": [1, 2]}))
    contract.analyze_merge(merge_id)
    assert contract.merged_sections(merge_id) == [left[0], right[1]]
    assert contract.conflict_indexes(merge_id) == []


def test_conflict_choice_requires_bilateral_author_approval(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    right = ["Access is available Monday through Thursday only.", BASE[1]]
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, right, "conflict")
    direct_vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": [4, 0]}))
    contract.analyze_merge(merge_id)
    contract.propose_conflict_choice(merge_id, 0, 1)
    direct_vm.sender = direct_bob
    contract.approve_resolutions(merge_id)
    assert contract.get_merge(merge_id)["state"] == "AWAITING_APPROVAL"
    direct_vm.sender = direct_charlie
    contract.approve_resolutions(merge_id)
    assert contract.get_merge(merge_id)["state"] == "SEALED"
    assert contract.merged_sections(merge_id)[0] == left[0]


def test_unlisted_wallet_cannot_approve(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    right = ["Access is available Monday through Thursday only.", BASE[1]]
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, right, "unauthorized")
    direct_vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": [4, 0]}))
    contract.analyze_merge(merge_id)
    contract.propose_conflict_choice(merge_id, 0, 2)
    direct_vm.sender = direct_accounts[3]
    with direct_vm.expect_revert("only_version_author"):
        contract.approve_resolutions(merge_id)


def test_model_cannot_contradict_exact_unchanged_text(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, BASE, BASE, "malformed")
    direct_vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": [4, 0]}))
    with direct_vm.expect_revert("[LLM_ERROR] relation_contradicts_exact_text"):
        contract.analyze_merge(merge_id)
