from fastapi import APIRouter
from tablemate_api.database import db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/")
async def get_restaurants():
    restaurants = await db.restaurants.find().to_list(length=100)  # Limit to 100 restaurants
    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])  
    return restaurants
