#This API will provide AI models using fastAPI
from typing import List
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
from schema import *
from routers import images, users, auth


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

app.include_router(images.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {'message': 'Welcome to my API'}
