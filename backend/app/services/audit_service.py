from datetime import datetime
from typing import Dict, Any


_audit_logs = []


def create_audit_log(
    payment: Dict[str, Any],
    decision: Dict[str, Any]
):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "payment_id": payment["payment_id"],
        "amount": float(payment["amount"]),
        "risk_score": decision["risk_score"],
        "diagnosis": decision["diagnosis"],
        "recommended_action": decision["recommended_action"],
        "policy_allowed": decision["policy_allowed"],
        "policy_reason": decision["policy_reason"],
        "final_action": decision["final_action"],
    }

    _audit_logs.append(log)

    return log


def get_audit_logs():
    return _audit_logs