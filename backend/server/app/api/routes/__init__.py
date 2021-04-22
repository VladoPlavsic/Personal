from fastapi import APIRouter

from app.api.routes.public import router as public_router
from app.api.routes.user import router as users_router


router = APIRouter()

router.include_router(public_router, prefix="/public", tags=["public"])
router.include_router(users_router, prefix="/authentication", tags=["authentication"])
