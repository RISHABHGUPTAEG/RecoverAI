# Architecture

Frontend Dashboard → FastAPI → Recovery Agent → Policy Engine → Recovery Service → Metrics + Audit Log

Critical money actions must be bounded and gated by deterministic policy checks.
