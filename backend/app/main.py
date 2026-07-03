from fastapi import FastAPI

app = FastAPI(
    title="GovCaptureAI",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "application": "GovCaptureAI",
        "version": "0.1.0",
        "status": "running"
    }