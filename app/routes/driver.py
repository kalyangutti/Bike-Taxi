from typing import List
from uuid import UUID

from fastapi import APIRouter
from pydantic import EmailStr

from app.database.dependencies import DriverServiceDep
from app.database.models import Gender
from app.schemas.driver import DriverCreate, DriverRespone, DriverUpdate
from app.schemas.user import PhoneNumber

router = APIRouter(prefix="/drivers", tags=["Driver"])


@router.get("/id", response_model=DriverRespone)
async def get_id_driver(id: UUID, service: DriverServiceDep):
    return await service.get_id(id)


@router.post("/register", response_model=DriverRespone)
async def create_driver(driver_creditinals: DriverCreate, service: DriverServiceDep):
    return await service.create_driver(driver_creditinals)


@router.patch("/update_driver", response_model=DriverRespone)
async def upadte_driver_details(
    id: UUID, driver_details: DriverUpdate, service: DriverServiceDep
):
    return await service.update_driver(id, driver_details)


@router.delete("/id")
async def delete_driver_by_uuid(id: UUID, service: DriverServiceDep):
    return await service.delete_driver(id)


@router.get("/sorting", response_model=List[DriverRespone])
async def custom_flitering(
    service: DriverServiceDep, sort_by: str = "name", order: str = "asc"
):
    return await service.sorting(sort_by, order)


@router.get("/pagination", response_model=DriverRespone)
async def pagination(
    service: DriverServiceDep,
    page: int = 1,
    size: int = 4,
    sort_by: str = "name",
    order: str = "asc",
):
    return await service.pagination(page, size, sort_by, order)


@router.get("/get_all_drivers")
async def get_all_drivers(service: DriverServiceDep):
    return await service.get_all_drivers()


@router.get("/get_driver_by_id", response_model=DriverRespone)
async def get_driver_by_id(service: DriverServiceDep, id: UUID):
    return await service.get_driver_by_id(id)


@router.get("/get_driver_by_email", response_model=DriverRespone)
async def get_driver_by_email(service: DriverServiceDep, email: EmailStr):
    return await service.get_driver_by_email(email)


@router.get("/get_driver_by_Phone", response_model=DriverRespone)
async def get_driver_by_phone(service: DriverServiceDep, phone: PhoneNumber):
    return await service.get_driver_by_phone(phone)


@router.get("/get_driver_by_age_greater_than", response_model=List[DriverRespone])
async def get_driver_by_age_greater_than(service: DriverServiceDep, age: int):
    return await service.get_driver_by_age_greater_than(age)


@router.get("/get_driver_by_age_lesser_than", response_model=List[DriverRespone])
async def get_driver_by_age_lesser_than(service: DriverServiceDep, age: int):
    return await service.get_driver_by_age_lesser_than(age)


@router.get("/get_driver_by_age_between", response_model=List[DriverRespone])
async def get_driver_by_age_between(
    service: DriverServiceDep, age_start: int, age_end: int
):
    return await service.get_driver_by_age_between(age_start, age_end)


@router.get("/get_driver_male", response_model=List[DriverRespone])
async def get_driver_male(service: DriverServiceDep):
    return await service.get_driver_male()


@router.get("/get_driver_female", response_model=List[DriverRespone])
async def get_driver_female(service: DriverServiceDep):
    return await service.get_driver_female()


@router.get("/get_driver_active", response_model=List[DriverRespone])
async def get_driver_active(service: DriverServiceDep):
    return await service.get_driver_active()


@router.get("/get_driver_inactive", response_model=List[DriverRespone])
async def get_driver_inactive(service: DriverServiceDep):
    return await service.get_driver_inactive()


@router.get("/get_driver_where_by_rides_less_than", response_model=List[DriverRespone])
async def get_driver_where_by_rides_less_than(service: DriverServiceDep, age: int):
    return await service.get_driver_where_by_rides_less_than(age)


@router.get(
    "/get_driver_where_by_rides_greater_than", response_model=List[DriverRespone]
)
async def get_driver_where_by_rides_greater_than(service: DriverServiceDep, age: int):
    return await service.get_driver_where_by_rides_greater_than(age)


@router.get("/get_drivers_where_by_rides_between", response_model=List[DriverRespone])
async def get_driver_get_drivers_where_by_rides_between(
    service: DriverServiceDep, ride_start: int, ride_end: int
):
    return await service.get_drivers_where_by_rides_between(ride_start, ride_end)


@router.get("/get_driver_where_contains_gmail", response_model=List[DriverRespone])
async def get_driver_where_contains_gmail(service: DriverServiceDep):
    return await service.get_driver_where_contains_gmail()


@router.get("/get_driver_name_startwith", response_model=List[DriverRespone])
async def get_driver_name_startwith(service: DriverServiceDep, name: str):
    return await service.get_driver_name_startwith(name)


@router.get("/get_driver_order_by_age", response_model=List[DriverRespone])
async def get_driver_order_by_age(service: DriverServiceDep):
    return await service.get_driver_order_by_age()


@router.get("/get_driver_order_by_rides", response_model=List[DriverRespone])
async def get_driver_order_by_rides(service: DriverServiceDep):
    return await service.get_driver_order_by_rides()


@router.get("/get_top_5_drivers", response_model=List[DriverRespone])
async def get_top_5_age_drivers(service: DriverServiceDep):
    return await service.get_top_5_age_drivers()


@router.get("/get_top_5_aged_drivers", response_model=List[DriverRespone])
async def get_top_5_highest_drivers(service: DriverServiceDep):
    return await service.get_top_5_highest_drivers()


@router.get("/get_name_start_with", response_model=List[DriverRespone])
async def get_name_start_with(service: DriverServiceDep, name: str):
    return await service.name_start_with(name)


@router.get("/get_name_ends_with", response_model=List[DriverRespone])
async def get_name_ends_with(service: DriverServiceDep, name: str):
    return await service.name_ends_with(name)


@router.get("/get_phone_number_startwith", response_model=List[DriverRespone])
async def get_phone_number_startwith(service: DriverServiceDep, phone: str):
    return await service.phone_number_startwith(phone)


@router.get("/get_phone_number_endS_with", response_model=List[DriverRespone])
async def get_phone_number_endS_with(service: DriverServiceDep, phone: str):
    return await service.phone_number_endS_with(phone)


@router.get("/get_phone_number_ends_with_com", response_model=List[DriverRespone])
async def get_phone_number_ends_with_com(service: DriverServiceDep, phone: str):
    return await service.phone_number_ends_with_com(phone)


@router.get(
    "/get_driver_details_whose_does_not_gmail", response_model=List[DriverRespone]
)
async def get_driver_details_whose_does_not_gmail(service: DriverServiceDep):
    return await service.get_driver_details_whose_does_not_gmail()


@router.get("/get_driver_details_by_age", response_model=List[DriverRespone])
async def get_driver_details_by_age(service: DriverServiceDep, age: int):
    return await service.get_driver_details_by_age(age)


@router.get("/get_driver_details_by_ride", response_model=List[DriverRespone])
async def get_driver_details_by_ride(service: DriverServiceDep, ride: int):
    return await service.get_driver_details_by_ride(ride)


@router.get("/get_driver_details_by_not_equal_age", response_model=List[DriverRespone])
async def get_driver_details_by_not_equal_age(service: DriverServiceDep, age: int):
    return await service.get_driver_details_by_not_equal_age(age)


@router.get(
    "/get_driver_details_by_not_equal_gender", response_model=List[DriverRespone]
)
async def get_driver_details_by_not_equal_gender(
    service: DriverServiceDep, gender: str
):
    return await service.get_driver_details_by_not_equal_gender(gender)


@router.get("/get_all_drivers_count")
async def get_total_drivers(service: DriverServiceDep):
    return await service.get_total_drivers()


@router.get("/get_all_drivers_active_or_inactive_count")
async def get_total_active_or_inactive(service: DriverServiceDep, active: bool):
    return await service.get_total_active_or_inactive(active)


@router.get("/get_total_male_or_female")
async def get_total_male_or_female(service: DriverServiceDep, gender: Gender):
    return await service.get_total_male_or_female(gender)


@router.get("/maximum_age_of_drivers")
async def maximum_age_of_drivers(service: DriverServiceDep):
    return await service.maximum_age_of_drivers()


@router.get("/minimum_age_of_drivers")
async def minimum_age_of_drivers(service: DriverServiceDep):
    return await service.minimum_age_of_drivers()


@router.get("/average_age_of_drivers")
async def average_age_of_drivers(service: DriverServiceDep):
    return await service.average_age_of_drivers()


@router.get("/total_number_rides")
async def total_number_rides(service: DriverServiceDep):
    return await service.total_number_rides()


@router.get("/average_age_of_driver_male")
async def average_age_of_driver_male(service: DriverServiceDep, gender: Gender):
    return await service.average_age_of_driver_male(gender)


@router.get("/count_drivers_by_gender_group_by")
async def count_drivers_by_gender_group_by(service: DriverServiceDep):
    return await service.count_drivers_by_gender_group_by()


@router.get("/total_rides_by_genders")
async def total_rides_by_gender(service: DriverServiceDep):
    return await service.total_rides_by_gender()


@router.get("/average_rides_by_gender")
async def average_rides_by_gender(service: DriverServiceDep):
    return await service.average_rides_by_gender()


@router.get("/maximum_rides_by_gender")
async def maximum_rides_by_gender(service: DriverServiceDep):
    return await service.maximum_rides_by_gender()


@router.get("/minimum_rides_by_gender")
async def minimum_rides_by_gender(service: DriverServiceDep):
    return await service.minimum_rides_by_gender()


@router.get("/count_drivers_by_ages")
async def count_drivers_by_ages(service: DriverServiceDep):
    return await service.count_drivers_by_ages()
