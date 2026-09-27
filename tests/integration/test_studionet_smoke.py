import json
import os
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address

from tests.studionet_support import emit_record, ok, source_schema_proof, wallet_accounts


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("RUN_STUDIONET") != "1", reason="opt-in live StudioNet test"),
]


def test_studionet_three_way_semantic_merge():
    accounts = wallet_accounts("versionmerge", 3)
    owner, left_author, right_author = accounts[:3]
    source = Path(__file__).resolve().parents[2] / "contracts" / "version_merge.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=owner)
    left_contract = factory.build_contract(address, account=left_author)
    right_contract = factory.build_contract(address, account=right_author)
    merge_id = f"{str(owner.address).lower()}:POLICY"
    base = ["Access is available on weekdays only.", "Reports are published every month."]
    left = ["Access is available every weekday and Saturday.", base[1]]
    right = [base[0], "Reports are published every two weeks."]
    setup = [ok(contract.open_merge(args=["policy", left_author.address, right_author.address, json.dumps(base), "Classify section relations and mark incompatible simultaneous changes as conflicts." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))]
    setup.append(ok(left_contract.submit_version(args=[merge_id, json.dumps(left)]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    setup.append(ok(right_contract.submit_version(args=[merge_id, json.dumps(right)]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    intelligent = ok(contract.analyze_merge(args=[merge_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    setup.append(ok(left_contract.approve_merge(args=[merge_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    setup.append(ok(right_contract.approve_merge(args=[merge_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED)))
    state = contract.get_merge(args=[merge_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "versionmerge/merge/v2" and state["state"] == "SEALED" and len(state["relations"]) == 2
    proof = source_schema_proof(address, source, {"submit_version", "analyze_merge", "approve_merge", "merged_sections", "conflict_indexes"})
    emit_record("versionmerge", "B", address, deployed, setup, intelligent, accounts, proof, {"state": state["state"], "relations": state["relations"], "conflicts": state["conflicts"], "authors_attested": state["left_submitted"] and state["right_submitted"]})
