from fastapi import APIRouter, HTTPException

from app.services.payment_service import (
    get_payment,
    get_failed_payments,
)

from app.agents.recovery_agent import analyze_payment


router = APIRouter(
    prefix="/api/recovery",
    tags=["Revenue Recovery"]
)


@router.get("/analyze/{payment_id}")
def analyze_single_payment(payment_id: str):

    payment = get_payment(payment_id)

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    if payment["status"] == "success":
        raise HTTPException(
            status_code=400,
            detail="Successful payment does not require recovery"
            )

    return analyze_payment(payment)


@router.get("/analyze-all")
def analyze_all_payments():

    payments = get_failed_payments()

    results = []

    for payment in payments:
        results.append(
            analyze_payment(payment)
        )

        return {
            "total_payments": len(results),
            "results": results
        }