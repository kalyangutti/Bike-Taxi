from fastapi import APIRouter, HTTPException, status

from app.schemas.driver import DriverCreate, DriverRead, DriverUpdate

router = APIRouter(prefix="/drivers", tags=["Driver"])

database = {
    1: {
        "name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "phone": "9876543210",
        "age": 24,
        "vehicle_number": "TN01AB1234",
        "password": "Rahul@123",
        "gender": "MALE",
        "is_active": True,
        "rides": 125,
    },
    2: {
        "name": "Arjun Kumar",
        "email": "arjun@gmail.com",
        "phone": "9123456789",
        "age": 27,
        "vehicle_number": "TN10CD5678",
        "password": "Arjun@123",
        "gender": "MALE",
        "is_active": True,
        "rides": 210,
    },
    3: {
        "name": "Kiran Reddy",
        "email": "kiran@gmail.com",
        "phone": "9988776655",
        "age": 29,
        "vehicle_number": "KA05EF4321",
        "password": "Kiran@123",
        "gender": "MALE",
        "is_active": False,
        "rides": 98,
    },
    4: {
        "name": "Sai Teja",
        "email": "sai@gmail.com",
        "phone": "9090909090",
        "age": 23,
        "vehicle_number": "AP16GH7890",
        "password": "Sai@1234",
        "gender": "MALE",
        "is_active": True,
        "rides": 56,
    },
    5: {
        "name": "Charan R",
        "email": "charan@gmail.com",
        "phone": "9012345678",
        "age": 26,
        "vehicle_number": "TS09JK1122",
        "password": "Charan@123",
        "gender": "MALE",
        "is_active": True,
        "rides": 175,
    },
}


# Get Drivers
@router.get("/id", response_model=DriverRead)
def get_driver(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return database[id]


# Get all Drivers
@router.get("/alldrivers")
def get_all_drivers():
    return database


# Search User
@router.get("/filter")
def search_user(field: str, value: str):
    result = []

    for driver in database.values():
        if str(driver.get(field)) == value:
            result.append(driver)

    return result


# Create  Driver
@router.post("/create")
def create_driver(body: DriverCreate):
    new_id = max(database.keys()) + 1
    database[new_id] = {**body.model_dump()}
    return {"Detail": f"New Id {new_id} has been created"}


# Update Driver Details
@router.patch("/updatedetails")
def update_driver_details(driver: DriverUpdate, driver_id: int):

    print("Before:", database[driver_id])

    details = driver.model_dump(exclude_unset=True)
    print("Received:", details)

    database[driver_id].update(details)

    print("After:", database[driver_id])

    return {"message": "Updated", "driver": database[driver_id]}


# Sorting
@router.get("/sort")
def sort_drivers(field: str, order: str = "asc"):

    drivers = list(database.values())

    reverse = order.lower() == "desc"

    sorted_drivers = sorted(drivers, key=lambda driver: driver[field], reverse=reverse)

    return sorted_drivers


# Pagination
@router.get("/offset")
def paginate_drivers(page: int, size: int):
    drivers = list(database.values())
    start = (page - 1) * size
    end = start + size
    return drivers[start:end]


# Delete Driver Details
@router.delete("/id")
def deleteDetails(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} not Found in the Database",
        )
    del database[id]
    return {"detail": f"Id of {id} database has been deleted"}
