from datetime import datetime

from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }
