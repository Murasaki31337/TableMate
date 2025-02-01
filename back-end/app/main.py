from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.database import client
from app.service.restaurant_service import RestaurantService
from app.service.reservation_service import ReservationService

app = FastAPI()

# Dependency Injection
def get_restaurant_service():
    return RestaurantService(client)

def get_reservation_service():
    return ReservationService(client)

class RestaurantIn(BaseModel):
    name: str
    address: str

class ReservationIn(BaseModel):
    customer_id: str
    restaurant_id: str
    table_id: str
    time: str

@app.post("/restaurants/register")
async def register_restaurant(restaurant: RestaurantIn, service: RestaurantService = Depends(get_restaurant_service)):
    try:
        return await service.register_restaurant(restaurant)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reservations")
async def create_reservation(reservation: ReservationIn, service: ReservationService = Depends(get_reservation_service)):
    try:
        return await service.create_reservation(reservation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
