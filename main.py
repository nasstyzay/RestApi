from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4, UUID

app = FastAPI()

class Advertisement(BaseModel):
    id: UUID
    title: str
    description: str
    price: float
    author: str
    created_at: datetime

class CreateAdvertisement(BaseModel):
    title: str
    description: str
    price: float
    author: str

advertisements = []

@app.post("/advertisement", response_model=Advertisement)
def create_advertisement(ad: CreateAdvertisement):
    new_ad = Advertisement(
        id=uuid4(),
        title=ad.title,
        description=ad.description,
        price=ad.price,
        author=ad.author,
        created_at=datetime.now()
    )
    advertisements.append(new_ad)
    return new_ad

@app.patch("/advertisement/{advertisement_id}", response_model=Advertisement)
def update_advertisement(advertisement_id: UUID, ad: CreateAdvertisement):
    for advertisement in advertisements:
        if advertisement.id == advertisement_id:
            advertisement.title = ad.title
            advertisement.description = ad.description
            advertisement.price = ad.price
            advertisement.author = ad.author
            return advertisement
    raise HTTPException(status_code=404, detail="Advertisement not found")

@app.delete("/advertisement/{advertisement_id}")
def delete_advertisement(advertisement_id: UUID):
    global advertisements
    advertisements = [ad for ad in advertisements if ad.id != advertisement_id]
    return {"message": "Deleted successfully"}

@app.get("/advertisement/{advertisement_id}", response_model=Advertisement)
def get_advertisement(advertisement_id: UUID):
    for advertisement in advertisements:
        if advertisement.id == advertisement_id:
            return advertisement
    raise HTTPException(status_code=404, detail="Advertisement not found")

@app.get("/advertisement", response_model=List[Advertisement])
def search_advertisements(
    title: Optional[str] = None,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    results = advertisements
    if title:
        results = [ad for ad in results if title.lower() in ad.title.lower()]
    if author:
        results = [ad for ad in results if author.lower() in ad.author.lower()]
    if min_price is not None:
        results = [ad for ad in results if ad.price >= min_price]
    if max_price is not None:
        results = [ad for ad in results if ad.price <= max_price]
    return results
