from fastapi import FastAPI

app = FastAPI(
    title="SecureFlow API",
    description="Cloud-native financial security platform",
    version="0.1.0",
)


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