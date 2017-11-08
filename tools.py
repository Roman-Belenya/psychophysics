from PIL import Image
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
	
	
def find_flicker_fs(frames, monitor_fs):
	return monitor_fs / float(frames)
	
def find_frames_in_cycle(flicker_fs, monitor_fs):
	return monitor_fs / float(flicker_fs)