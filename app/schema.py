from pydantic import BaseModel, EmailStr
from datetime import datetime

#Class to validate prompts to create and edit images
class ImageBase(BaseModel):
    prompt: str

class ImageCreate(ImageBase):
    pass

class ImageResponse(BaseModel):
    path_image: str
    prompt:     str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name:     str
    email:    EmailStr
    password: str

class UserResponse(BaseModel):
    id:       int
    name:     str
    email:    EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
