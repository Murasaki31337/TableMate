from app.dal.restaurant_dal import RestaurantRepository
from app.models.restaurant import Restaurant
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

class RestaurantService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.repo = RestaurantRepository(db_client)

    async def register_restaurant(self, restaurant_in: BaseModel):
        if await self.repo.get_restaurant_by_name(restaurant_in.name):
            raise Exception("Restaurant already registered.")
        restaurant = Restaurant(**restaurant_in.dict())
        return await self.repo.save_restaurant(restaurant)

    async def get_restaurant(self, restaurant_id: str):
        return await self.repo.get_restaurant_by_id(restaurant_id)
