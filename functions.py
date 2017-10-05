from PIL import *
import numpy as np

def change_colour(image, dim = 0, by = 2./256):

    assert np.all(image >= -1) and np.all(image <= 1), 'Some pixels outside -1:1 range'
    img = image.copy()
    mask = np.zeros(img.shape, dtype = np.bool) # create a 3d boolean mask
    nonwhite = img[:,:,2] != 1 # 2 because changed value in this dimension when making it red/green
    mask[:,:,dim] = nonwhite # insert all non-white pixels from to image to the dim in mask as True
    img[mask] += by

    return img

	

def prepare_image(image, fg_colour = 0, bg_colour = 0):


	img = np.flip(
			np.array(
				Image.open(image)
					) / 127.5 - 1,
				0)

	fg = img == -1
	img[fg] = fg_colour		# change colour of drawing
	img[~fg] = bg_colour	# ~background = foreground 
	return img
