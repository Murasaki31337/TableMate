from fastapi import APIRouter, HTTPException
from tablemate_api.database import db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/")
async def get_restaurants():
    restaurants = await db.restaurants.find().to_list(length=100)  # Limit to 100 restaurants
    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])  
    return restaurants


@router.get("/{name}")
async def get_restaurant_by_name(name: str):
    try:
        restaurant = await db.restaurants.find_one({"name": name})
        if restaurant:
            restaurant["_id"] = str(restaurant["_id"])  
            return restaurant
        else:
            raise HTTPException(status_code=404, detail="Restaurant not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Name format: {e}")

@router.get("/{restaurant_name}/reservations")
async def get_reservation_details(restaurant_name: str):
    restaurant = await db.reservations.find_one({"restaurant_name": restaurant_name})

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found.")

    # Return the restaurant name and table types
    return {
        "restaurant_name": restaurant["restaurant_name"],
        "table_types": restaurant["table_types"]
    }

@router.post("/reservations")
async def make_reservation(reservation: dict):
    restaurant_name = reservation.get("restaurant_name")
    table_type = reservation.get("table_type")

    if not restaurant_name or not table_type:
        raise HTTPException(status_code=400, detail="Restaurant name and table type are required.")

    # Find the restaurant in the database by its name
    restaurant = await db.reservations.find_one({"restaurant_name": restaurant_name})

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found.")

    # Check if the selected table type is available
    if table_type not in restaurant["table_types"]:
        raise HTTPException(status_code=400, detail="Selected table type not available.")

    # Reserve the table (this is simplified, you may want to adjust this logic)
    restaurant["table_types"][table_type] -= 1

    # If no available tables left, return an error
    if restaurant["table_types"][table_type] < 0:
        raise HTTPException(status_code=400, detail="No tables available for the selected type.")

    # Update the reservation status
    await db.reservations.update_one(
        {"restaurant_name": restaurant_name},
        {"$set": {"table_types": restaurant["table_types"]}}
    )

    return {"message": "Reservation successful!"}