from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "AI Customer Support Ticket System is running"
    }