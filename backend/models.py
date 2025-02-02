from pydantic import BaseModel, Field

# Pydantic Models
class ItemBase(BaseModel):
    name: str
    description: str
    price: float

class ItemModel(ItemBase):
    id: str = Field(default_factory=str)

# Helper function to serialize MongoDB documents
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item["description"],
        "price": item["price"]
    }
