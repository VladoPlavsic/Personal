from fastapi import APIRouter

from app.api.routes.user import router as test_router

router = APIRouter()

router.include_router(test_router, prefix="/authentication", tags=["authentication"])
