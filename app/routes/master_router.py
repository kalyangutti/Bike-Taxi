from fastapi import APIRouter

from app.routes.driver import router as driver_router
from app.routes.health import router as health_router
from app.routes.rider import router as rider_router

router = APIRouter()

router.include_router(health_router)
router.include_router(rider_router)
router.include_router(driver_router)
