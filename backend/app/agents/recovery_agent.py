from typing import Dict, Any

from app.agents.policy_engine import evaluate_policy


def calculate_risk(payment: Dict[str, Any]) -> int:
    score = 0

    status = payment.get("status")
    reason = payment.get("reason", "")
    days = int(payment.get("days_since_failure", 0))
    customer_type = payment.get("customer_type", "regular")
    amount = float(payment.get("amount", 0))

    # Failed payment
    if status == "failed":
        score += 30

        if reason == "insufficient_funds":
            score += 25

        elif reason == "bank_declined":
            score += 30

        elif reason == "timeout":
            score += 15

        elif reason == "checkout_timeout":
            score += 20

    # Abandoned checkout
    elif status == "abandoned":
        score += 20

        if reason == "checkout_timeout":
            score += 20

    # Older failures increase recovery risk
    if days >= 3:
        score += 20

    elif days == 2:
        score += 10

    # Premium customers
    if customer_type == "premium":
        score += 10

    # High-value transactions
    if amount >= 15000:
        score += 10

    return min(score, 100)


def diagnose_payment(payment: Dict[str, Any]) -> str:
    reason = payment.get("reason", "")

    if reason == "insufficient_funds":
        return (
            "Customer may have insufficient balance. "
            "A payment reminder is safer than repeated retries."
        )

    if reason == "bank_declined":
        return (
            "Bank declined the transaction. "
            "A controlled retry or alternate payment reminder may recover the payment."
            )

    if reason == "timeout":
        return (
            "Payment appears to have timed out. "
            "A controlled retry may be appropriate."
            )

    if reason == "checkout_timeout":
        return (
            "Checkout was abandoned or timed out. "
            "A checkout reminder can recover the customer."
            )

    return "Payment requires manual review."


def choose_action(payment: Dict[str, Any], risk_score: int) -> str:
    status = payment.get("status")
    reason = payment.get("reason", "")
    days = int(payment.get("days_since_failure", 0))

    if days > 3:
        return "escalate"

    if status == "abandoned":
        return "send_checkout_reminder"

    if reason == "insufficient_funds":
        return "send_payment_reminder"

    if reason == "timeout" and days <= 2:
        return "retry_payment"

    if reason == "bank_declined":
        return "send_payment_reminder"

    if risk_score >= 70:
        return "escalate"

    return "send_payment_reminder"


def analyze_payment(payment: Dict[str, Any]) -> Dict[str, Any]:
    risk_score = calculate_risk(payment)

    diagnosis = diagnose_payment(payment)

    action = choose_action(payment, risk_score)

    policy = evaluate_policy(payment, action)

    final_action = action if policy["allowed"] else "escalate"

    return {
        "payment_id": payment["payment_id"],
        "amount": float(payment["amount"]),
        "risk_score": risk_score,
        "diagnosis": diagnosis,
        "recommended_action": action,
        "policy_allowed": policy["allowed"],
        "policy_reason": policy["reason"],
        "final_action": final_action,
        }