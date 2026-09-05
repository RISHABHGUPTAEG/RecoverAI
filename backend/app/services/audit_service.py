from datetime import datetime
from typing import Dict, Any

_audit_logs = []


def calculate_demo_recovery(
    payment: Dict[str, Any],
    decision: Dict[str, Any]
):
    amount = float(payment["amount"])
    action = decision["final_action"]

    recovery_rates = {
        "retry_payment": 0.35,
        "send_payment_reminder": 0.30,
        "send_checkout_reminder": 0.40,
    }

    rate = recovery_rates.get(action, 0)

    if rate == 0:
        return {
            "outcome": "not_recovered",
            "recovered_amount": 0,
        }

    recovered_amount = round(amount * rate, 2)

    return {
        "outcome": "recovered",
        "recovered_amount": recovered_amount,
    }


def create_audit_log(
    payment: Dict[str, Any],
    decision: Dict[str, Any]
):
    existing = next(
        (
            log
            for log in _audit_logs
            if log["payment_id"] == payment["payment_id"]
        ),
        None,
    )

    if existing:
        return {
            **existing,
            "duplicate": True,
        }

    outcome = calculate_demo_recovery(payment, decision)

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
        "outcome": outcome["outcome"],
        "recovered_amount": outcome["recovered_amount"],
        "duplicate": False,
    }

    _audit_logs.append(log)

    return log


def get_audit_logs():
    return _audit_logs


def get_measured_recovered():
    return round(
        sum(
            log["recovered_amount"]
            for log in _audit_logs
        ),
        2,
    )
