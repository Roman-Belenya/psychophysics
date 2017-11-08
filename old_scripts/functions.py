from PIL import *
import numpy as np

    
def get_fg_mask(image):
    # returns psyhopy mask of black pixel locations
    # 1 = transparent, -1 = opaque
    
    img = np.flip(np.array(Image.open(image)), 0)
    fg = from_rgb(img[:,:,0]) * -1

    return fg
    
    
def from_rgb(value):
    assert np.all(value >= 0) and np.all(value <= 255), 'Invalid value'
    
    return value / 127.5 - 1
    
    
def to_rgb(value):
    assert np.all(value >= -1) and np.all(value <= 1), 'Invalid value in {}'.format(np.unique(value))

    v = 255 + np.around((value - 1) * 127.5)
    return int(v)
    
   
def change_colour(colour, by):
	
	new_colour = colour + by
	
	if np.any(new_colour < 0) or np.any(new_colour > 255):
		print 'out of range'
		return colour
	
	return new_colour
	
	
def deg_to_cm(degs, d):
	return 2 * d * np.tan(degs/2.0)
	
def cm_to_deg(cms, d):
	return 2 * np.atan(cms/(2.0*d))
	
	
	
	
def _change_colour(image, dim = 0, by = 2./256):

    img = image.copy()
    mask = np.zeros(img.shape, dtype = np.bool) # create a 3d boolean mask
    nonwhite = img[:,:,2] != 1 # 2 because changed value in this dimension when making it red/green
    mask[:,:,dim] = nonwhite # insert all non-white pixels from to image to the dim in mask as True
    img[mask] += by
    
    level = np.unique(img[mask])[0]
    
    if np.any(img > 1) or np.any(img < -1):
        print 'Some values outside -1:1 range. returning original'
        return image, None

    return img, level

    
def prepare_image(image, fg_colour = 0, bg_colour = 0):


    img = np.flip(
            np.array(
                Image.open(image)
                    ) / 127.5 - 1,
                0)

    fg = img == -1
    img[fg] = fg_colour        # change colour of drawing
    img[~fg] = bg_colour    # ~background = foreground 
    return img