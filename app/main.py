#This API will provide AI models using fastAPI

from fastapi import FastAPI,Response,status, Depends
from fastapi.exceptions import HTTPException
import openai
import psycopg2
from psycopg2.extras import RealDictCursor

import os  
from PIL import Image  
import shutil
import time
from sqlalchemy.orm import Session

from  config import settings
import models
from database import engine, get_db
import utils
from schema import ImageCreate, ImageResponse

models.Base.metadata.create_all(bind=engine)

# set API key
openai.api_key = settings.OPENAI_APIKEY

path_image = 'static\images'

#Path to save images
if os.path.exists("static\images") == False: os.mkdir("static\images")
if os.path.exists("static\mask") == True: shutil.rmtree("static\mask") 

os.mkdir("static\mask")

#API instance
app = FastAPI()

#Retrieve all elements in db
@app.get("/images", status_code=status.HTTP_200_OK)
def get_all_images(db: Session = Depends(get_db)):
    print('[LOG] Request received')
    images = db.query(models.Image).all()
    return images

@app.get('/images/{image_id}', status_code=status.HTTP_200_OK, response_model=ImageResponse)
def get_one_image(image_id: int, db: Session = Depends(get_db)):
    print('[LOG] Request received for image_id: %s', image_id)
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    return image 

#Create Image
@app.post("/images", status_code=status.HTTP_201_CREATED, response_model=ImageResponse)
def create_image(item: ImageCreate, db: Session = Depends(get_db)):
    print('[LOG] Prompt received, starting generation')
    generation_response = utils.generation_response(item.prompt)
    path= utils.save_image(generation_response)
    new_image = models.Image(path_image=path,prompt = item.prompt)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

#Modify Image
@app.put("/images/{image_id}", status_code=status.HTTP_201_CREATED,response_model=ImageResponse)
def edit_image(item: ImageCreate, image_id: int, db: Session = Depends(get_db)):
    image_query = db.query(models.Image).filter(models.Image.id == image_id)
    image = image_query.first()

    if image == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id: {image_id} does not exist')
    
    img_path = os.path.join(path_image,image.path_image)

    if img_path: 
        print('[LOG] Image found')
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id: {image_id} not found in the server')
    
    print('[LOG] Starting edition')
    mask_path = utils.mask(img_path)
    utils.edit_image(img_path, mask_path, item.prompt, image.path_image)
    print('[LOG] Image successfully edited')
    #image_query = db.query(models.Image).filter(models.Image.id == image_id)
    #print(image.prompt +' / '+ item.prompt)
    image.prompt = image.prompt +' / '+ item.prompt
    db.commit()
    db.refresh(image)
    return image

@app.delete('/images/{image_id}')
def del_image(image_id: int, db: Session = Depends(get_db)):
    image_query = db.query(models.Image).filter(models.Image.id == image_id)
    image = image_query.first()
    print('[LOG] Image found in server')
    if image == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id: {image_id} not found')
    
    image_query.delete()
    db.commit()

    del_im = os.path.join(path_image, image.path_image)
    os.remove(del_im)
    print('[LOG] Image deleted from server')

    return Response(status_code = status.HTTP_204_NO_CONTENT)
