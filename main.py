#This API will provide AI models using fastAPI

from fastapi import FastAPI,Response,status
import openai
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

import os  
from PIL import Image  
import shutil
import time
from src.config import settings

from src import utils

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host = settings.POSTGRES_HOST, database = settings.POSTGRES_DB,
                                user = settings.POSTGRES_USER, password = settings.POSTGRES_PASSWORD,
                                cursor_factory=RealDictCursor)
        
        # Open a cursor to perform database operations
        cursor = conn.cursor()  #To execute sql entries 
        print('[LOG] Database successfully connected')
        break

    except Exception as error:
        print('[Error] Connecting to database failed', error)
        time.sleep(3)

#Class to validate prompts
class Item(BaseModel):
    prompt: str

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
@app.get("/images")
def get_all_images():
    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()
    if images != []:
        print('[LOG] Retrieving elements in db')
        message = images
    else:
        print('[LOG] No elements in db')
        message = 'No elements in db'
   
    return {'images': message}

#Create Image
@app.post("/images")
def create_image(item: Item):
    print('[LOG] Prompt received, starting generation')
    generation_response = utils.generation_response(item.prompt)
    path= utils.save_image(generation_response)
    cursor.execute("""INSERT INTO images (path_image,prompt) VALUES (%s,%s) RETURNING *;""", (path,item.prompt))
    new_image = cursor.fetchone()
    conn.commit()
    return {'message': new_image}

#Modify Image
@app.put("/images/{image_id}")
def edit_image(item: Item, image_id: int):
    SQL = """SELECT * FROM images WHERE id = (%s);"""
    data = (image_id,)
    cursor.execute(SQL,data)
    try:
        image = dict(cursor.fetchone())
        print('[LOG] Image found')
        print('[LOG] Starting edition')
        img_path = os.path.join(path_image,image['path_image'])
        mask_path = utils.mask(img_path)
        utils.edit_image(img_path, mask_path, item.prompt, image['path_image'])
        message = "Image successfully edited"
    except Exception as error:
        print('[LOG] Image not found, try another id')
        message = "Image not found, try another id"

    return {'message': message}

@app.delete('/images/{image_id}')
def del_image(image_id: int):
    cursor.execute("""SELECT * FROM images WHERE id = %s;""", (str(image_id),))
    try:
        deleted_image = dict(cursor.fetchone())
        del_im = os.path.join(path_image, deleted_image['path_image'])
        os.remove(del_im)
        print('[LOG] Image deleted from server')
    except Exception as error:
        print('[LOG] Image not found in server')

    cursor.execute("""DELETE FROM images WHERE id = %s RETURNING *;""", (str(image_id),))
    deleted_image = cursor.fetchone()
    conn.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)
