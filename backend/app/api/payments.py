from fastapi import APIRouter, HTTPException

from app.services.payment_service import (
    load_payments,
    get_payment,
    get_failed_payments,
)

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.get("/")
def payments():
    return {
        "count": len(load_payments()),
        "payments": load_payments()
        }


@router.get("/failed")
def failed_payments():
    data = get_failed_payments()

    return {
        "count": len(data),
        "payments": data
        }


@router.get("/{payment_id}")
def payment(payment_id: str):
    data = get_payment(payment_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return data