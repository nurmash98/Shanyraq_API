from pydantic import BaseModel
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