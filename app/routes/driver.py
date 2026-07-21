from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/drivers", tags=["Driver"])

database = {
    1: {"name": "Rahul", "phone": "9876543210", "vehicle_number": "TN01AB1234"},
    2: {"name": "Arjun", "phone": "9123456789", "vehicle_number": "TN10CD5678"},
    3: {"name": "Kiran", "phone": "9988776655", "vehicle_number": "KA05EF4321"},
    4: {"name": "Sai", "phone": "9090909090", "vehicle_number": "AP16GH7890"},
    5: {"name": "Charan", "phone": "9012345678", "vehicle_number": "TS09JK1122"},
}


# Get all drivers
@router.get("/")
def get_all_drivers():
    return database


# Get driver by ID
@router.get("/{id}")
def get_driver(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )
    return database[id]


# Create driver
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_driver(name: str, phone: str, vehicle_number: str):
    new_id = max(database.keys(), default=0) + 1

    database[new_id] = {
        "name": name,
        "phone": phone,
        "vehicle_number": vehicle_number,
    }

    return {"id": new_id, "driver": database[new_id]}


# Update driver
@router.patch("/{id}")
def update_driver(
    id: int,
    name: str | None = None,
    phone: str | None = None,
    vehicle_number: str | None = None,
):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )

    if name is not None:
        database[id]["name"] = name

    if phone is not None:
        database[id]["phone"] = phone

    if vehicle_number is not None:
        database[id]["vehicle_number"] = vehicle_number

    return {"message": "Driver updated successfully", "driver": database[id]}


# Delete driver
@router.delete("/{id}")
def delete_driver(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )

    deleted_driver = database.pop(id)

    return {"message": "Driver deleted successfully", "driver": deleted_driver}
