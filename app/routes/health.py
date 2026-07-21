from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def get_message():
    return {"message": "welcome to Bike Taxi API"}

@router.get('/healthy')
def get_healthy():
    return {"status":"healthy"}


