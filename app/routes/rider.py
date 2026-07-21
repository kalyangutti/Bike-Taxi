from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/rider", tags=["Rider"])


database = {
    1: {"name": "Drake", "phone": "9014929583"},
    2: {"name": "Vamsi", "phone": "9848012345"},
    3: {"name": "Rahul", "phone": "9876543210"},
    4: {"name": "Arjun", "phone": "9123456789"},
    5: {"name": "Kiran", "phone": "9988776655"},
    6: {"name": "Sai", "phone": "9090909090"},
    7: {"name": "Akhil", "phone": "9012345678"},
    8: {"name": "Charan", "phone": "9876501234"},
    9: {"name": "Harsha", "phone": "9988001122"},
    10: {"name": "Rohit", "phone": "9345678901"},
    11: {"name": "Nikhil", "phone": "9556677889"},
    12: {"name": "Surya", "phone": "9000011111"},
    13: {"name": "Teja", "phone": "9112233445"},
    14: {"name": "Pavan", "phone": "9887766554"},
    15: {"name": "Manoj", "phone": "9776655443"},
}


@router.get("/alluser")
def get_all():
    return database


@router.get("/user")
def get_id(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} not Found"
        )
    return database[id]


@router.post("/user")
def create_user(name: str, phone: str):
    new_id = max(database.keys()) + 1
    database[new_id] = {"name": name, "phone": phone}
    return {"new_id": f"Data with {new_id} is created"}


@router.patch("/user")
def update_user(id: int, name: str | None = None, phone: str | None = None):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Detail With {id} is created"
        )
    if name is not None:
        database[id]["name"] = name
    if phone is not None:
        database[id]["phone"] = phone

    return {"detail": f"Data with the Id  {id} Updated"}


@router.delete("/user")
def delete_user(id: int):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is Not Found"
        )
    del database[id]
    return {"detail": f"Data With {id} is deleted"}
