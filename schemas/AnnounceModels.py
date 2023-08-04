from pydantic import BaseModel
from typing import Optional
class PostAnnouncement(BaseModel):
    type: str
    price: int 
    address: str 
    area: int 
    rooms_count: int 
    description: str 

class UpdateAnnouncement(BaseModel):
    type: str
    price: int
    address: str
    area: int 
    rooms_count: int
    description: str

class QueryAnnouncement(BaseModel):
    limit: int | None = None
    offset: int | None = None
    type: str = "sell"
    rooms_count: int = 1
    price_from: int = 0
    price_until: int = 1000000000
