from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.payments import router as payments_router
from app.api.recovery import router as recovery_router
from app.api.routes import router as routes_router
from app.api.metrics import router as metrics_router

app = FastAPI(
    title="RecoverAI",
    description="AI-Powered Revenue Recovery Agent",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(payments_router)
app.include_router(recovery_router)
app.include_router(routes_router)
app.include_router(metrics_router)


@app.get("/")
def root():
    return {
"app": "RecoverAI",
"status": "running",
"message": "AI Revenue Recovery Agent is online"
}


@app.get("/health")
def health():
    return {
"status": "healthy"
}