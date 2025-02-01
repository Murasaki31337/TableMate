from motor.motor_asyncio import AsyncIOMotorClient
from app.models.reservation import Reservation
from typing import Optional
from bson import ObjectId

class ReservationRepository:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client.tablemate
        self.collection = self.db.reservations

    async def save_reservation(self, reservation: Reservation):
        result = await self.collection.insert_one(reservation.dict())
        return {"id": str(result.inserted_id)}

    async def get_reservation_by_id(self, reservation_id: str) -> Optional[Reservation]:
        reservation = await self.collection.find_one({"_id": ObjectId(reservation_id)})
        return Reservation(**reservation) if reservation else None
