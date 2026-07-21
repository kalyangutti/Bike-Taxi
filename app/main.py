from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.routes.master_router import router as master_router

app = FastAPI()


app.include_router(master_router)


@app.get("/info")
def get_info():
    return {
        "app_name": "Bike Taxi API",
        "Version": "1.0.0",
        "environment": "development",
    }


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="SCALAR API")
