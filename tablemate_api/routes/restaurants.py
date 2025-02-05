from fastapi import APIRouter
from tablemate_api.database import db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/")
async def get_restaurants():
    restaurants = await db.restaurants.find().to_list(length=100)  # Limit to 100 restaurants
    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])  
    return restaurants


@router.get("/{id}")
async def get_restaurant_by_id(id: str):
    try:
        restaurant = await db.restaurants.find_one({"_id": ObjectId(id)})
        if restaurant:
            restaurant["_id"] = str(restaurant["_id"])  
            return restaurant
        else:
            raise HTTPException(status_code=404, detail="Restaurant not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ID format: {e}")