from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "payments.csv"


def load_payments():
    df = pd.read_csv(DATA_FILE)

    df = df.fillna("")

    return df.to_dict(orient="records")


def get_payment(payment_id: str):
    payments = load_payments()

    for payment in payments:
        if payment["payment_id"] == payment_id:
            return payment

        return None


def get_failed_payments():
    payments = load_payments()

    return [
payment
for payment in payments
if payment["status"] in ["failed", "abandoned"]
]