import fastapi

from src import endpoints


app = fastapi.FastAPI(
    title="TronGeteway",
    description="Service for interacting with the TronGeteway.",
    version="2.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(endpoints.app)
