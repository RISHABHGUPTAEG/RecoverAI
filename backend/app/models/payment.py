from pydantic import BaseModel
from typing import Optional


class Payment(BaseModel):
    payment_id: str
    customer_id: str
    amount: float
    status: str
    reason: Optional[str] = None
    days_since_failure: int = 0
    customer_type: str = "regular"