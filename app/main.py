from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.shortener import router as shortener_router

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "A production-style distributed URL shortening platform "
        "evolving from a simple CRUD backend to a complete distributed system."
    ),
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Enable CORS for future frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"], summary="API Health Check")
async def health_check():
    """
    Standard health check endpoint to verify that the application service is running properly.
    """
    return {"status": "healthy", "service": settings.APP_NAME}

# Register URL shortener router
app.include_router(shortener_router)
