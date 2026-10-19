from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.transactions import router as transactions_router
from app.api.auth import router as auth_router


app = FastAPI(
    title="SecureFlow API",
    description="Cloud-native financial security platform",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

app.swagger_ui_parameters = {
    "url": "/api/openapi.json",
}

app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "application": "SecureFlow",
        "status": "running",
        "message": "Secure financial operations platform",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }