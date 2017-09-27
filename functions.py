from PIL import *
import numpy as np

def change_colour(image, dim = 0, by = +10):

    assert np.all(0 <= image) and np.all(image <= 255), 'Some pixels outside 8-bit values'
    img = image.copy() # img[img[:,:,dim] != 255] += by # changes entries in all dimensions
    mask = np.zeros(image.shape, dtype = np.bool) # create a 3d boolean mask
    nonwhite = img[:,:,dim] != 255
    mask[:,:,dim] = nonwhite # insert all non-white pixels from to image to the dim in mask as True
    img[mask] += by
	
    return img
	
# def prepare_image(img):
	# img = Image.open(img)
	
	# green = np.array(img); print green.shape
	# green[:,:,1] = 255
	# red = np.array(img)
	# red[:,:,0] = 255
		
	# green = green/127.5 - 1 # convert to [-1, 1] for psychopy
	# red = red/127.5 - 1
	
	# green = np.flip(green, 0) # flip horizontally
	# red = np.flip(red, 0)
	
	# return green, red
	
def prepare_image(image, fg_colour = 0):


	img = np.flip(
			np.array(
				Image.open(image)
					) / 127.5 - 1,
				0)
	
	fg = img == -1
	img[fg] = fg_colour		# change colour of drawing 
	img[~fg] = 0			# background is always grey
	
	return img