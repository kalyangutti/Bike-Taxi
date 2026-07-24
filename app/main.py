from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.database.session import create_database_tables
from app.routes.master_router import router as master_router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Server Started...")
    await create_database_tables()
    yield
    print("..Server Stopped")


app = FastAPI(lifespan=lifespan_handler)


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
