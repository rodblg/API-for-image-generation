# API-for-image-generation

This is an API conecting to the OPENAI API for image generation using the DALL-E motors. It has the CRUD
operations to read all images saved, read one image, update/edit an image and also delete a specific image. 
It has a postgresql database integrated to save the prompts and path of each image to be able to find them and edit them.
To edit an image with DALL-E is necessary to use a mask of the image to edit where the transparent regions
is where the system updates the new changes.
I use a different method than OpenAI for the mask generation to edit images as I am only using backend in the API. For this mask I choosed a K means algorithm to find the region of the image where there was a bigger area of pixels with the same label. Although the system is able to modify existing images, the editing options are limitated due to the unsupervised method for the mask generation.

