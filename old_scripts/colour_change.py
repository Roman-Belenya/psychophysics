import numpy as np
from PIL import Image
import time
import matplotlib.pyplot as plt

imgPath = ".\line_drawings\converted\square.png"

img = Image.open(imgPath)
arr = np.array(img)
print arr.shape

print arr[:,:,0]
print

def timer(func):
	def inside(*args, **kwargs):
		t0 = time.time()
		res = func(*args, **kwargs)
		t1 = time.time() - t0
		print t1
		return res, t1
	return inside
	
# @timer	
def change_colour(image, dim = 0, by = +10):

    assert np.all(0 <= image) and np.all(image <= 255), 'Some pixels outside 8-bit values'
    img = image.copy() # img[img[:,:,dim] != 255] += by # changes entries in all dimensions
    mask = np.zeros(image.shape, dtype = np.bool) # create a 3d boolean mask
    nonwhite = img[:,:,dim] != 255
    mask[:,:,dim] = nonwhite # insert all non-white pixels from to image to the dim in mask as True
    img[mask] += by
	
    return img
	
	
print np.unique(arr)
i = change_colour(arr, dim = 0, by = 128)
print i[:,:,0]
print
print i[:,:,1]
print
print i[:,:,2]
print i.shape


Image.fromarray(i).show()