import openai

import os
import requests

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 
from datetime import datetime

image_dir = "static\images"
image_dir_mask = "static\mask"

def generation_response(prompt):
    generation_response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="url",
    )
    return generation_response

def save_image(generation_response):
    now = datetime.now()
    time = now.strftime("%d%m%Y_%H%M%S")
    generated_image_name = "generated_image_"+time+".jpg"  # any name you like; the filetype should be .png
    generated_image_filepath = os.path.join(image_dir, generated_image_name)
    generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(generated_image_url).content  # download the image
    with open(generated_image_filepath, "wb") as image_file:
        image_file.write(generated_image)  # write the image to the file
    return generated_image_name


def mask(im_path):
    image = cv2.imread(im_path)
    # cv2 read images in BGR format so we convert it back to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)
    # define stopping criteria to stop kmeans
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    # We define the number of clusters (K = 3) but it can be changed always > 1
    k = 3 
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # convert back to 8 bit values
    centers = np.uint8(centers)
    # flatten the labels array
    labels = labels.flatten()
    # convert all pixels to the color of the centroids
    segmented_image = centers[labels.flatten()]
    # reshape back to the original image dimension, image with the pixel segmentation
    segmented_image = segmented_image.reshape(image.shape)
    

    masked_image = np.copy(image)
    # convert to the shape of a vector of pixel values
    masked_image = masked_image.reshape((-1, 3))
    #Identify largest label of pixels
    cluster = np.argmax(np.bincount(labels))
    #Define the region of the mask as 0
    masked_image[labels == cluster] = [0, 0, 0]
    # convert back to original shape
    masked_image = masked_image.reshape(image.shape)
    mask = Image.fromarray(masked_image).convert('RGBA')

    #We make that 0 region transparent
    edit = mask.getdata()
    newData = []
    for item in edit:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    mask.putdata(newData)
    mask_image_filepath = os.path.join(image_dir_mask, "mask.png")
    mask.save(mask_image_filepath)
    return mask_image_filepath

def edit_image(image,mask,prompt,path_image):
    response = openai.Image.create_edit(
    image=open(image, "rb"),
    mask=open(mask, 'rb'),
    prompt=prompt,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    path_image = os.path.join(image_dir,path_image)
    generated_image_edit_name = path_image
    generated_image_edit = requests.get(image_url).content  # download the image
    with open(generated_image_edit_name, "wb") as image_file:
        image_file.write(generated_image_edit)  # write the image to the file