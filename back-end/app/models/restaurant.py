from pydantic import BaseModel
from typing import Optional

class Restaurant(BaseModel):
    id: Optional[str] = None
    name: str
    address: str
    owner_id: str  # Owner's user ID
