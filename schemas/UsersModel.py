from pydantic import BaseModel, validator
import re
class CreateUser(BaseModel):
    username: str
    phone: str
    password: str 
    name: str
    city: str

    @validator("username")
    def validate_email(cls, value):
        if not re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', value):
            raise ValueError('Invalid email address')
        return value
    
    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", value):
            raise ValueError('Invalid phone number')
        return value
    

class UpdateUser(BaseModel):
    phone: str 
    name: str
    city: str

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", value):
            raise ValueError('Invalid phone number')
        return value
    
class GetUserResponse(BaseModel):
    id: int
    username: str
    phone: str
    name: str
    ciyt: str