
from fastapi import FastAPI,Response,status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from typing import List
import os

import models, schema, utils, oauth2
from database import get_db

router = APIRouter(
    prefix='/images',
    tags = ['images']
)


path_image = 'static\images'


#Retrieve all elements in db
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.ImageResponse])
def get_all_images(db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    
    print('[LOG] Request received')
    images = db.query(models.Image).all()
    return images

@router.get('/{image_id}', status_code=status.HTTP_200_OK, response_model=schema.ImageResponse)
def get_one_image(image_id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    print('[LOG] Request received for image_id: %s', image_id)
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    return image 

#Create Image
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.ImageResponse)
def create_image(item: schema.ImageCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.name)
    print('[LOG] Prompt received, starting generation')
    generation_response = utils.generation_response(item.prompt)
    path= utils.save_image(generation_response)
    print(path)
    new_image = models.Image(path_image=path,prompt = item.prompt, owner_id=current_user.id)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

#Modify Image
@router.put("/{image_id}", status_code=status.HTTP_201_CREATED,response_model=schema.ImageResponse)
def edit_image(item: schema.ImageCreate, image_id: int, db: Session = Depends(get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    image_query = db.query(models.Image).filter(models.Image.id == image_id)
    image = image_query.first()

    if image == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id: {image_id} does not exist')
    
    if image.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to performe current action')
    
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

@router.delete('/{image_id}')
def del_image(image_id: int, db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user)):
    
    image_query = db.query(models.Image).filter(models.Image.id == image_id)
    image = image_query.first()
    print('[LOG] Image found in server', image)
    if image == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Image with id: {image_id} not found')
    
    if image.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to performe current action')

    if image != None:
        del_im = os.path.join(path_image, image.path_image)
        print(del_im)
        os.remove(del_im)

    image_query.delete()
    db.commit()    
    print('[LOG] Image deleted from server')

    return Response(status_code = status.HTTP_204_NO_CONTENT)

