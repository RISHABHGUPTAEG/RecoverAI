from typing import Dict, Any


MAX_RETRY_DAYS = 3
MIN_RECOVERY_AMOUNT = 100
MAX_AUTO_RECOVERY_AMOUNT = 20000


def evaluate_policy(payment: Dict[str, Any], action: str) -> Dict[str, Any]:
    amount = float(payment["amount"])
    days = int(payment.get("days_since_failure", 0))

    # Minimum amount check
    if amount < MIN_RECOVERY_AMOUNT:
        return {
            "allowed": False,
            "reason": "Payment amount is below recovery threshold",
        }

    # Recovery window check
    if days > MAX_RETRY_DAYS:
        return {
            "allowed": False,
            "reason": "Recovery window expired",
            }

    # High-value payment check
    if amount > MAX_AUTO_RECOVERY_AMOUNT:
        return {
            "allowed": False,
            "reason": "High-value payment requires manual approval",
            }

    # Allowed recovery actions
    allowed_actions = {
        "retry_payment",
        "send_payment_reminder",
        "send_checkout_reminder",
        "escalate",
    }

    if action not in allowed_actions:
        return {
            "allowed": False,
            "reason": "Unknown recovery action",
            }

    # Retry-specific restriction
    if action == "retry_payment" and days > 2:
        return {
            "allowed": False,
            "reason": "Automatic retry limit reached",
            }

    # Everything passed
    return {
        "allowed": True,
        "reason": "Action passed recovery policy",
        }