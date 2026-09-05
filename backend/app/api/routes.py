from fastapi import APIRouter

from app.services.payment_service import get_failed_payments
from app.agents.recovery_agent import analyze_payment
from app.services.audit_service import (
    create_audit_log,
    get_audit_logs,
)


router = APIRouter(
    prefix="/api",
    tags=["Recovery System"]
)


@router.post("/recover/{payment_id}")
def execute_recovery(payment_id: str):

    payments = get_failed_payments()

    payment = next(
        (
            p for p in payments
            if p["payment_id"] == payment_id
        ),
        None
    )

    if not payment:
        return {
            "success": False,
            "message": "Payment not eligible for recovery"
        }

    decision = analyze_payment(payment)

    audit = create_audit_log(
        payment,
        decision
    )

    return {
        "success": True,
        "decision": decision,
        "audit": audit
    }


@router.get("/audit")
def audit_logs():

    return {
        "count": len(get_audit_logs()),
        "logs": get_audit_logs()
        }