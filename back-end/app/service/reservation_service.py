from app.dal.reservation_dal import ReservationRepository
from app.models.reservation import Reservation
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

class ReservationService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.repo = ReservationRepository(db_client)

    async def create_reservation(self, reservation_in: BaseModel):
        reservation = Reservation(**reservation_in.dict())
        return await self.repo.save_reservation(reservation)
