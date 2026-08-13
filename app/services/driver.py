from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc, desc, func, select

from app.database.models import Driver, Gender
from app.schemas.driver import DriverCreate, DriverUpdate
from app.schemas.user import PhoneNumber
from app.security import password_hash


class DriverRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_id(self, id: UUID):
        driver = await self.session.get(Driver, id)

        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Driver with id {id} not found.",
            )

        return driver

    async def create_driver(self, driver_create: DriverCreate):
        driver = Driver(
            **driver_create.model_dump(
                exclude={"password", "created_at", "updated_at"}
            ),
            password=password_hash.hash(driver_create.password),
        )

        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)

        return driver

    async def update_driver(self, id: UUID, driver_update: DriverUpdate):
        driver = await self.get_id(id)

        update_data = driver_update.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided.",
            )

        driver.sqlmodel_update(update_data)

        self.session.add(driver)
        await self.session.commit()
        await self.session.refresh(driver)

        return driver

    async def delete_driver(self, id: UUID):
        driver = await self.get_id(id)

        await self.session.delete(driver)
        await self.session.commit()

        return {"message": f"Driver {id} deleted successfully."}

    async def sorting(self, sort_by: str = "name", order: str = "asc"):
        column = getattr(Driver, sort_by, None)

        if column is None:
            raise ValueError("Invalid Sorting Field")

        stmt = select(Driver)
        if order.lower() == "desc":
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))

        result = await self.session.scalars(stmt)

        return result.all()

    async def pagination(
        self, page: int = 1, size=4, sort_by: str = "name", order: str = "asc"
    ):
        column = getattr(Driver, sort_by, "None")

        if column is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Sorting Field"
            )

        offset = (page - 1) * size

        stmt = select(Driver)

        if order.lower() == "desc":
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))

        stmt = stmt.offset(offset).limit(size)

        result = await self.session.scalars(stmt)
        return result.all()

    async def get_all_drivers(self):
        stmt = select(Driver)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_by_id(self, id: UUID):
        stmt = select(Driver).where(Driver.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_driver_by_email(self, email: EmailStr):
        stmt = select(Driver).where(Driver.email == email)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_driver_by_phone(self, phone: PhoneNumber):
        stmt = select(Driver).where(Driver.phone == phone)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_driver_by_age_greater_than(self, age: int):
        stmt = select(Driver).where(Driver.age > age)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_by_age_lesser_than(self, age: int):
        stmt = select(Driver).where(Driver.age < age)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_by_age_between(self, age_start: int, age_end: int):
        stmt = select(Driver).where(Driver.age.between(age_start, age_end))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_male(self):
        stmt = select(Driver).where(Driver.gender == "MALE")
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_female(self):
        stmt = select(Driver).where(Driver.gender == "FEMALE")
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_active(self):
        stmt = select(Driver).where(Driver.is_active == True)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_inactive(self):
        stmt = select(Driver).where(Driver.is_active == False)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_where_by_rides_less_than(self, rides: int):
        stmt = select(Driver).where(Driver.rides < rides)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_where_by_rides_greater_than(self, rides: int):
        stmt = select(Driver).where(Driver.rides > rides)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_drivers_where_by_rides_between(self, ride_start: int, ride_end: int):
        stmt = select(Driver).where(Driver.rides.between(ride_start, ride_end))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_where_contains_gmail(self):
        stmt = select(Driver).where(Driver.email.like("%gmail.com"))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_name_startwith(self, name: str):
        stmt = select(Driver).where(Driver.name.startswith(name))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_order_by_age(self):
        stmt = select(Driver).order_by(Driver.age)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_order_by_rides(self):
        stmt = select(Driver).order_by(Driver.rides)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_top_5_age_drivers(self):
        stmt = select(Driver).order_by(Driver.age.desc()).limit(5)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_top_5_highest_drivers(self):
        stmt = select(Driver).order_by(Driver.rides.desc()).limit(5)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def name_start_with(self, name: str):
        stmt = select(Driver).where(Driver.name.startswith(name))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def name_ends_with(self, name: str):
        stmt = select(Driver).where(Driver.name.endswith(name))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def phone_number_startwith(self, phone: str):
        stmt = select(Driver).where(Driver.phone.startswith(phone))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def phone_number_endS_with(self, phone: str):
        stmt = select(Driver).where(Driver.phone.endswith(phone))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def phone_number_ends_with_com(self, email: str):
        stmt = select(Driver).where(Driver.email.endswith(email))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_driver_details_whose_does_not_gmail(self):
        stmt = select(Driver).where(Driver.email.notlike("%gmail%"))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_driver_details_by_age(self, age):
        stmt = select(Driver).where(Driver.age == age)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_driver_details_by_ride(self, rides):
        stmt = select(Driver).where(Driver.rides == rides)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_driver_details_by_not_equal_age(self, age):
        stmt = select(Driver).where(Driver.age != age)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_driver_details_by_not_equal_gender(self, gender):
        stmt = select(Driver).where(Driver.gender != gender)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_total_drivers(self):
        stmt = select(func.count(Driver.id))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_total_active_or_inactive(self, active: bool):
        stmt = select(func.count(Driver.id)).where(Driver.is_active == active)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_total_male_or_female(self, gender: Gender):
        stmt = select(func.count(Driver.id)).where(Driver.gender == gender)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def maximum_age_of_drivers(self):
        stmt = select(func.max(Driver.age))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def minimum_age_of_drivers(self):
        stmt = select(func.min(Driver.age))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def average_age_of_drivers(self):
        stmt = select(func.avg(Driver.age))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def maximum_number_of_rides(self):
        stmt = select(func.max(Driver.rides))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def minimum_number_of_rides(self):
        stmt = select(func.min(Driver.rides))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def average_number_of_rides(self):
        stmt = select(func.avg(Driver.rides))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def total_number_rides(self):
        stmt = select(func.count(Driver.rides))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def average_age_of_driver_male(self, gender: Gender):
        stmt = select(Driver.gender, func.avg(Driver.age)).group_by(Driver.gender)
        result = await self.session.execute(stmt)
        return result.mappings().all()


    async def count_drivers_by_gender_group_by(self):
        stmt = (
            select(
                Driver.gender,
                func.count(Driver.id).label("Count")
            )
            .group_by(Driver.gender)
        )

        result = await self.session.execute(stmt)
        return result.mappings().all()




    async def total_rides_by_gender(self):
        stmt = (select(Driver.gender,func.sum(Driver.rides).label('Total no of Rides')).group_by(Driver.gender))
        res = await self.session.execute(stmt)
        return res.mappings().all()



    async def average_rides_by_gender(self):
        stmt = (select(Driver.gender,func.avg(Driver.rides).label("Average No of  Rides")).group_by(Driver.gender))
        res = await self.session.execute(stmt)
        return res.mappings().all()



    async def maximum_rides_by_gender(self):
        stmt = select(
            Driver.gender, func.max(Driver.rides).label("Highest No of  Rides")
        ).group_by(Driver.gender)
        res = await self.session.execute(stmt)
        return res.mappings().all()


    async def minimum_rides_by_gender(self):
        stmt = (select(Driver.gender,func.min(Driver.rides).label("Minimum No of Rides")).group_by(Driver.gender))
        res = await self.session.execute(stmt)
        return res.mappings().all()



    async def count_drivers_by_ages(self):
        stmt = (select(
            Driver.age,
            func.count(Driver.id).label("Count no of Drivers per Age"),
        ).group_by(Driver.age))

        res = await self.session.execute(stmt)
        return res.mappings().all()
