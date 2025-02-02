from fastapi import FastAPI, HTTPException
from typing import List
from bson import ObjectId

from backend.models import ItemBase, ItemModel, item_helper
from backend.database import items_collection
from backend.middleware import add_cors

app = FastAPI()

# Add CORS middleware
add_cors(app)

@app.get("/")
async def check():
    return {"message": "hello"}

@app.post("/items/", response_model=ItemModel)
async def create_item(item: ItemBase):
    item_dict = item.dict()
    result = await items_collection.insert_one(item_dict)
    created_item = await items_collection.find_one({"_id": result.inserted_id})
    return item_helper(created_item)

@app.get("/items/", response_model=List[ItemModel])
async def read_items(skip: int = 0, limit: int = 100):
    items_cursor = items_collection.find().skip(skip).limit(limit)
    items = []
    async for item in items_cursor:
        items.append(item_helper(item))
    return items

@app.get("/items/{item_id}", response_model=ItemModel)
async def get_item(item_id: str):
    if (item := await items_collection.find_one({"_id": ObjectId(item_id)})) is not None:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=ItemModel)
async def update_item(item_id: str, item_update: ItemBase):
    updated_item = await items_collection.find_one_and_update(
        {"_id": ObjectId(item_id)},
        {"$set": item_update.dict()},
        return_document=True
    )
    if updated_item:
        return item_helper(updated_item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = await items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
