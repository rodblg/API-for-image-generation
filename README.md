# API-for-image-generation

On this repository I use OpenAI API to access to the DALL-E motors with my own API. It has the 4 CRUD operations to create new images, edit them and delete them. 
It also has a postgresql database integrated to save the prompts and path of each image to be able to find them and edit them. 
I use a different method than OpenAI for the mask generation to edit images as I am only using backend to work with the images. For this mask I choosed
a k means algorithm to find the region of the image where there was a bigger area of pixels with the same label. Although the system is able to modify existing images,
the editing options are limitated due to the unsupervised method for the mask generation.

