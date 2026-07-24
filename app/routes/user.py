from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserDetailsUpdate, UserRead

router = APIRouter(prefix="/user", tags=["User"])


database = {
    1: {
        "name": "Rahul Sharma",
        "age": 24,
        "email": "rahul.sharma@gmail.com",
        "phone": "9876543210",
        "gender": "MALE",
        "password": "Rahul@123",
        "created_at": datetime(2026, 7, 24, 10, 30, 45),
        "updated_at": datetime(2026, 7, 24, 10, 30, 45),
    },
    2: {
        "name": "Priya Reddy",
        "age": 22,
        "email": "priya.reddy@gmail.com",
        "phone": "9123456789",
        "gender": "FEMALE",
        "password": "Priya@123",
        "created_at": datetime(2026, 7, 20, 9, 15, 10),
        "updated_at": datetime(2026, 7, 22, 14, 45, 30),
    },
    3: {
        "name": "Arjun Kumar",
        "age": 27,
        "email": "arjun.kumar@gmail.com",
        "phone": "9012345678",
        "gender": "MALE",
        "password": "Arjun@123",
        "created_at": datetime(2026, 7, 18, 11, 5, 20),
        "updated_at": datetime(2026, 7, 23, 18, 10, 5),
    },
    4: {
        "name": "Sneha Patel",
        "age": 25,
        "email": "sneha.patel@gmail.com",
        "phone": "9988776655",
        "gender": "FEMALE",
        "password": "Sneha@123",
        "created_at": datetime(2026, 7, 15, 16, 20, 15),
        "updated_at": datetime(2026, 7, 24, 8, 0, 0),
    },
    5: {
        "name": "Vikram Singh",
        "age": 29,
        "email": "vikram.singh@gmail.com",
        "phone": "9871234567",
        "gender": "MALE",
        "password": "Vikram@123",
        "created_at": datetime(2026, 7, 10, 13, 40, 50),
        "updated_at": datetime(2026, 7, 21, 17, 30, 25),
    },
}


# ALL USER
@router.get("/alluser")
def get_all():
    return database


# Reterive User By Id
@router.get("/byid", response_model=UserRead)
def get_id(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Id {id} not present in database",
        )

    return database[id]


# Create User
@router.post("/register")
def create_user(body: UserCreate):
    max_id = max(database.keys()) + 1
    database[max_id] = {**body.model_dump()}
    return {"detail": f"Id {max_id}"}


# update User Details
@router.patch("/update_details")
def updateDetails(id: int, body: UserDetailsUpdate):
    details = body.model_dump(exclude_unset=True)

    print("Recived : ", database[id])

    database[id].update(details)

    print("Updated:", database[id])
    return {"message": "Updated", "driver": database[id]}


@router.delete("/id")
def deleteDetails(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not found in Database"
        )
    del database[id]
    return {"detail": f"Id {id} deleted form the database."}


@router.get("/sort")
def sorting(field: str, order: str = "asc"):
    users = list(database.values())

    reverse = order.lower() == "desc"

    sorted_users = sorted(users, key=lambda user: user[field], reverse=reverse)

    return sorted_users


@router.get("/offset")
def pagination(page: int, size: int):
    users = list(database.values())
    start = (page - 1) * size
    end = start + size
    return users[start:end]


@router.get("/sortingoffset")
def custom_sorting_pagination(
    field: str,
    order: str = "asc",
    page: int = 1,
    size: int = 3,
):
    users = list(database.values())

    if field not in users[0]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{field}' is not a valid field.",
        )

    reverse = order.lower() == "desc"

    sorted_users = sorted(users, key=lambda user: user[field], reverse=reverse)

    start = (page - 1) * size
    end = start + size

    return sorted_users[start:end]
