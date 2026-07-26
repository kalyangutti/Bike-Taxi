from fastapi import APIRouter

from app.routes.driver import router as driver_router
from app.routes.health import router as health_router
from app.routes.user import router as rider_router
from app.routes.vehicle import router as vehicle_router

router = APIRouter()

router.include_router(health_router)
router.include_router(rider_router)
router.include_router(driver_router)
router.include_router(vehicle_router)
