from fastapi import APIRouter

from app.services.payment_service import get_failed_payments
from app.agents.recovery_agent import analyze_payment


router = APIRouter(
    prefix="/api/metrics",
    tags=["Metrics"]
)


@router.get("/")
def get_metrics():

    payments = get_failed_payments()

    total_at_risk = 0
    recoverable_amount = 0
    recovered_amount = 0

    action_counts = {
        "retry_payment": 0,
        "send_payment_reminder": 0,
        "send_checkout_reminder": 0,
        "escalate": 0,
    }

    results = []

    for payment in payments:

        amount = float(payment["amount"])

        decision = analyze_payment(payment)

        total_at_risk += amount

        if decision["policy_allowed"]:
            recoverable_amount += amount

            action = decision["final_action"]

            if action in action_counts:
                action_counts[action] += 1

                results.append({
                    **payment,
                    **decision
                })

                # Demo recovery simulation.
                # Only payments with a recovery action are counted.
                for payment in results:
                    if payment["final_action"] in [
                        "retry_payment",
                        "send_payment_reminder",
                        "send_checkout_reminder"
                    ]:
                        recovered_amount += payment["amount"] * 0.35

                        recovery_rate = (
                            (recovered_amount / total_at_risk) * 100
                            if total_at_risk > 0
                            else 0
                        )

                        return {
                            "total_transactions": len(payments),
                            "total_at_risk": round(total_at_risk, 2),
                            "recoverable_amount": round(recoverable_amount, 2),
                            "estimated_recovered": round(recovered_amount, 2),
                            "recovery_rate": round(recovery_rate, 2),
                            "action_counts": action_counts,
                            "transactions": results
                        }