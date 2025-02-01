from motor.motor_asyncio import AsyncIOMotorClient
from app.models.restaurant import Restaurant
from typing import Optional
from bson import ObjectId

class RestaurantRepository:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client.tablemate
        self.collection = self.db.restaurants

    async def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        restaurant = await self.collection.find_one({"_id": ObjectId(restaurant_id)})
        return Restaurant(**restaurant) if restaurant else None

    async def get_restaurant_by_name(self, name: str) -> Optional[Restaurant]:
        restaurant = await self.collection.find_one({"name": name})
        return Restaurant(**restaurant) if restaurant else None

    async def save_restaurant(self, restaurant: Restaurant):
        result = await self.collection.insert_one(restaurant.dict())
        return {"id": str(result.inserted_id)}
