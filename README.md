# API-for-image-generation

It also has a postgresql database integrated to save the prompts and path of each image to be able to find them and edit them.
I use a different method than OpenAI for the mask generation to edit images as I am only using backend to work with the images. For this mask I choosed
a K means algorithm to find the region of the image where there was a igger area of pixels with the same label. Although the system is able to modify existing images,
the editing options are limitated due to the unsupervised method for the mask generation.

