#This API will provide AI models using fastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai

import os   
import shutil
from sqlalchemy.orm import Session

import models,utils, database, config
from routers import images, users, auth

#models.Base.metadata.create_all(bind=database.engine)

# set API key
openai.api_key = config.settings.OPENAI_APIKEY

path_image = 'static\images'

#Path to save images
if os.path.exists("static\images") == False: os.mkdir("static\images")
if os.path.exists("static\mask") == True: shutil.rmtree("static\mask") 

os.mkdir("static\mask")

#API instance
app = FastAPI()

origins = ['https://www.google.com.mx']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def main():
    return {"message": "Hello World"}