from fastapi import APIRouter, HTTPException
from tablemate_api.database import db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/")
async def get_restaurants():
    restaurants = await db.restaurants.find().to_list(length=100)  # Limit to 100 restaurants
    for restaurant in restaurants:
        restaurant["_id"] = str(restaurant["_id"])  
    return restaurants

@router.post("/")
async def create_restaurant(restaurant: dict):
    """
    Add a new restaurant to the database.
    """
    name = restaurant.get("name")
    address = restaurant.get("address")
    details = restaurant.get("details")

    # Validate input fields
    if not name or not address or not details:
        raise HTTPException(status_code=400, detail="All fields (name, address, details) are required.")

    # Check if a restaurant with the same name already exists
    existing_restaurant = await db.restaurants.find_one({"name": name})
    if existing_restaurant:
        raise HTTPException(status_code=400, detail="Restaurant already exists")

    # Insert into MongoDB
    new_restaurant = {"name": name, "address": address, "details": details}
    result = await db.restaurants.insert_one(new_restaurant)
    await db.reservations.insert_one({
        "restaurant_name": name,
        "table_types": {
            "couple": 20,
            "family": 20,
            "party": 20
        }
    })

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create restaurant")

    return {"message": "Restaurant created successfully", "restaurant_id": str(result.inserted_id)}


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


@router.put("/name/{restaurant_name}")
async def update_restaurant(restaurant_name: str, update_data: dict):
    existing_restaurant = await db.restaurants.find_one({"name": restaurant_name})
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    update_query = {k: v for k, v in update_data.items() if v is not None}
    if not update_query:
        raise HTTPException(status_code=400, detail="No valid data provided")

    result = await db.restaurants.update_one({"name": restaurant_name}, {"$set": update_query})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update restaurant.")

    return {"message": "Restaurant updated successfully"}



# 2️⃣ **Update Reservation Quantity**
@router.put("/name/{restaurant_name}/reservations/update")
async def update_reservation(restaurant_name: str, update_data: dict):
    """
    Update the reservation quantity for a specific table type in a restaurant.
    """
    table_type = update_data.get("table_type")
    quantity = update_data.get("quantity")

    if not table_type or quantity is None or quantity <= 0:
        raise HTTPException(status_code=400, detail="Table type and quantity are required")

    restaurant = await db.restaurants.find_one({"name": restaurant_name})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    update_query = {f"table_types.{table_type}": quantity}
    result = await db.reservations.update_one({"restaurant_name": restaurant_name}, {"$set": update_query})

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update reservation")

    return {"message": f"Reservation for {table_type} updated to {quantity}"}

@router.patch("/name/{restaurant_name}/reservations/update")
async def update_reservation(restaurant_name: str, update_data: dict):
    """
    Update the reservation quantity for a specific table type in a restaurant.
    """
    table_type = update_data.get("table_type")
    quantity = update_data.get("quantity")

    if not table_type or quantity is None:
        raise HTTPException(status_code=400, detail="Table type and quantity are required")

    # Query the reservations collection instead of restaurants
    reservation = await db.reservations.find_one({"restaurant_name": restaurant_name})
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation data not found for this restaurant")

    # Fix the incorrect key usage
    update_query = {f"table_types.{table_type}": reservation["table_types"].get(table_type, 0) + quantity}
    
    result = await db.reservations.update_one({"restaurant_name": restaurant_name}, {"$set": update_query})

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update reservation")

    return {"message": f"Reservation for {table_type} updated to {reservation['table_types'][table_type] + quantity}"}


@router.delete("/name/{restaurant_name}")
async def delete_restaurant(restaurant_name: str):
    """
    Delete a restaurant by name, along with its associated reservations.
    """
    # Find the restaurant
    restaurant = await db.restaurants.find_one({"name": restaurant_name})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Delete the restaurant
    delete_result = await db.restaurants.delete_one({"name": restaurant_name})
    delete_result = await db.reservations.delete_one({"restaurant_name": restaurant_name})
    # If no restaurant was deleted
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete restaurant")

    # Also remove any reservations linked to this restaurant
    await db.reservations.delete_one({"restaurant_name": restaurant_name})

    return {"message": f"Restaurant '{restaurant_name}' and its reservations have been deleted successfully."}

