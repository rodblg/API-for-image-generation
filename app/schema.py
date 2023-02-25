from pydantic import BaseModel

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

