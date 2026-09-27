import json


POLICY = "Classify semantic changes section by section and mark incompatible simultaneous changes as conflicts."
BASE = ["Access is available on weekdays only.", "Reports are published every month."]


def _address(value):
    if isinstance(value, (bytes, bytearray)):
        return "0x" + bytes(value).hex()
    return str(value)


def _open(contract, vm, owner, left_author, right_author, key="policy"):
    vm.sender = owner
    return contract.open_merge(key, left_author, right_author, json.dumps(BASE), POLICY)


def _ready(contract, vm, owner, left_author, right_author, left, right, key="policy"):
    merge_id = _open(contract, vm, owner, left_author, right_author, key)
    vm.sender = left_author
    contract.submit_version(merge_id, json.dumps(left))
    vm.sender = right_author
    contract.submit_version(merge_id, json.dumps(right))
    vm.sender = owner
    return merge_id


def _analyze(contract, vm, merge_id, relations):
    vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": relations}))
    contract.analyze_merge(merge_id)


def test_authors_attest_independent_versions_and_bilaterally_seal_conflict_free_merge(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    right = [BASE[0], "Reports are published every two weeks."]
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, right)
    _analyze(contract, direct_vm, merge_id, [1, 2])
    state = contract.get_merge(merge_id)
    assert state["schema"] == "versionmerge/merge/v2"
    assert state["state"] == "AWAITING_APPROVAL"
    assert contract.merged_sections(merge_id) == [left[0], right[1]]
    direct_vm.sender = direct_bob
    contract.approve_merge(merge_id)
    assert contract.get_merge(merge_id)["state"] == "AWAITING_APPROVAL"
    direct_vm.sender = direct_charlie
    contract.approve_merge(merge_id)
    assert contract.get_merge(merge_id)["state"] == "SEALED"


def test_conflict_choice_requires_bilateral_author_approval(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    right = ["Access is available Monday through Thursday only.", BASE[1]]
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, right, "conflict")
    _analyze(contract, direct_vm, merge_id, [4, 0])
    contract.propose_conflict_choice(merge_id, 0, 1)
    direct_vm.sender = direct_bob
    contract.approve_merge(merge_id)
    direct_vm.sender = direct_charlie
    contract.approve_merge(merge_id)
    assert contract.get_merge(merge_id)["state"] == "SEALED"
    assert contract.merged_sections(merge_id)[0] == left[0]


def test_owner_cannot_impersonate_version_author(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "owner-submit")
    with direct_vm.expect_revert("only_version_author"):
        contract.submit_version(merge_id, json.dumps(BASE))
    assert contract.get_merge(merge_id)["left_submitted"] is False
    assert contract.get_merge(merge_id)["right_submitted"] is False


def test_outsider_cannot_submit_version(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "outsider-submit")
    direct_vm.sender = direct_accounts[3]
    with direct_vm.expect_revert("only_version_author"):
        contract.submit_version(merge_id, json.dumps(BASE))


def test_author_cannot_replace_submitted_version(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "replace")
    direct_vm.sender = direct_bob
    contract.submit_version(merge_id, json.dumps(BASE))
    with direct_vm.expect_revert("version_already_submitted"):
        contract.submit_version(merge_id, json.dumps([BASE[0], "Reports are published every week."]))


def test_submission_must_match_base_section_count(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "count")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("section_count_mismatch"):
        contract.submit_version(merge_id, json.dumps([BASE[0], BASE[1], "A third unexpected section."]))


def test_analysis_waits_for_both_authors(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    merge_id = _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "not-ready")
    direct_vm.sender = direct_bob
    contract.submit_version(merge_id, json.dumps(BASE))
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("versions_not_ready"):
        contract.analyze_merge(merge_id)


def test_only_owner_can_analyze_ready_merge(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, BASE, BASE, "owner-only")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.analyze_merge(merge_id)


def test_unlisted_wallet_cannot_approve(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, BASE, BASE, "unauthorized")
    _analyze(contract, direct_vm, merge_id, [0, 0])
    direct_vm.sender = direct_accounts[3]
    with direct_vm.expect_revert("only_version_author"):
        contract.approve_merge(merge_id)


def test_conflict_choice_is_owner_only_and_single_use(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    right = ["Access is available Monday through Thursday only.", BASE[1]]
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, right, "choice")
    _analyze(contract, direct_vm, merge_id, [4, 0])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.propose_conflict_choice(merge_id, 0, 1)
    direct_vm.sender = direct_alice
    contract.propose_conflict_choice(merge_id, 0, 2)
    with direct_vm.expect_revert("merge_has_no_open_conflicts"):
        contract.propose_conflict_choice(merge_id, 0, 1)


def test_model_cannot_contradict_exact_unchanged_text(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, BASE, BASE, "contradiction")
    direct_vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": [4, 0]}))
    with direct_vm.expect_revert("[LLM_ERROR] relation_contradicts_exact_text"):
        contract.analyze_merge(merge_id)


def test_model_must_return_one_closed_relation_code_per_section(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    left = ["Access is available every weekday and Saturday.", BASE[1]]
    merge_id = _ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie, left, BASE, "malformed")
    direct_vm.mock_llm(r".*Classify each aligned base-left-right section relation.*", json.dumps({"relations": [1]}))
    with direct_vm.expect_revert("[LLM_ERROR] wrong_relation_count"):
        contract.analyze_merge(merge_id)


def test_role_addresses_must_be_distinct_and_nonzero(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("author_roles_must_be_distinct"):
        contract.open_merge("same", _address(direct_alice), direct_charlie, json.dumps(BASE), POLICY)
    with direct_vm.expect_revert("author_address_is_zero"):
        contract.open_merge("zero", "0x" + "0" * 40, direct_charlie, json.dumps(BASE), POLICY)


def test_owner_merge_key_is_unique(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "duplicate")
    with direct_vm.expect_revert("merge_exists"):
        _open(contract, direct_vm, direct_alice, direct_bob, direct_charlie, "duplicate")
