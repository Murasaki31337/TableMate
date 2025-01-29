from pydantic import BaseModel
from typing import Optional

class Reservation(BaseModel):
    id: Optional[str] = None
    customer_id: str
    restaurant_id: str
    table_id: str
    time: str
