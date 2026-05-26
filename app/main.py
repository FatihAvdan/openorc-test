from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4


class Item(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


app = FastAPI(title="FastAPI App", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items: List[Item] = []


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/items", response_model=List[Item])
async def list_items():
    return items


@app.post("/api/items", response_model=Item, status_code=201)
async def create_item(item_in: ItemCreate):
    item = Item(id=str(uuid4()), name=item_in.name, description=item_in.description)
    items.append(item)
    return item


@app.get("/api/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    for item in items:
        if item.id == item_id:
            return item
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/items/{item_id}", status_code=204)
async def delete_item(item_id: str):
    from fastapi import HTTPException
    for i, item in enumerate(items):
        if item.id == item_id:
            items.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")
