from datetime import datetime
from fastapi import FastAPI
from src.api.v1 import recipes, batches

app = FastAPI(
    title="Brewery App API",
    description="API de gestión de cervecería artesana",
    version="0.1.0"
)

# Registrar routers con su prefijo y tag para Swagger
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["recipes"])
app.include_router(batches.router, prefix="/api/v1/batches", tags=["batches"])


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }
