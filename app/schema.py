from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#Class to validate prompts to create and edit images
class ImageBase(BaseModel):
    prompt: str

class ImageCreate(ImageBase):
    pass

class ImageResponse(BaseModel):
    path_image: str
    prompt:     str
    id:         int
    owner_id:    int
    created_at: datetime
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type:   str

class TokenData(BaseModel):
    id: Optional[str] = None
