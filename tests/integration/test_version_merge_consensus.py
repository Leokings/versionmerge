import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.contracts.contract import Contract
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _contract(address, account):
    # glsim 0.1 does not recognize the pinned SDK's generated contract wrapper
    # when deriving a schema. StudioNet supplies its native schema; locally,
    # gltest only needs the method names and write/view distinction.
    methods = {
        "open_merge": False,
        "submit_version": False,
        "analyze_merge": False,
        "propose_conflict_choice": False,
        "approve_merge": False,
        "get_merge": True,
        "merged_sections": True,
        "conflict_indexes": True,
    }
    schema = {
        "ctor": {"params": [], "kwparams": {}},
        "methods": {
            name: {"params": [], "kwparams": {}, "ret": "any", "readonly": readonly}
            for name, readonly in methods.items()
        },
    }
    return Contract.new(address=address, schema=schema, account=account)


def test_five_validator_three_way_merge():
    owner, left_author, right_author = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "version_merge.py")
    receipt = factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    address = extract_contract_address(receipt)
    contract = _contract(address, owner)
    left_contract = _contract(address, left_author)
    right_contract = _contract(address, right_author)
    merge_id = f"{str(owner.address).lower()}:POLICY"
    base = ["Access is available on weekdays only.", "Reports are published every month."]
    left = ["Access is available every weekday and Saturday.", base[1]]
    right = [base[0], "Reports are published every two weeks."]
    _ok(contract.open_merge(args=["policy", left_author.address, right_author.address, json.dumps(base), "Classify semantic changes section by section and mark incompatible simultaneous changes as conflicts." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(left_contract.submit_version(args=[merge_id, json.dumps(left)]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(right_contract.submit_version(args=[merge_id, json.dumps(right)]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Classify each aligned base-left-right section relation": json.dumps({"relations": [1, 2]})}})
    context = {"validators": [v.to_dict() for v in validators], "genvm_datetime": "2026-08-25T12:00:00Z"}
    _ok(contract.analyze_merge(args=[merge_id]).transact(transaction_context=context, wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.merged_sections(args=[merge_id]).call() == [left[0], right[1]]
    _ok(left_contract.approve_merge(args=[merge_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(right_contract.approve_merge(args=[merge_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.get_merge(args=[merge_id]).call()["state"] == "SEALED"
