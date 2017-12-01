from PIL import Image
import numpy as np
from psychopy import monitors
import matplotlib.pyplot as plt
import os


def create_monitor(name, distance, width_cm, dim_pix):
    '''create_monitor(distance = 40 cm, width_cm = 53.13, dim_pix = [1920, 1080])'''

    mon = monitors.Monitor(name = name)
    mon.setWidth(width_cm)
    mon.setDistance(distance)
    mon.setSizePix(dim_pix)
    mon.saveMon()


def get_fg_mask(image):
    '''returns psyhopy mask of black pixel locations where 1 = transparent, -1 = opaque '''

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

def invert(colour):
    if isinstance(colour, list):
        colour = np.array(colour)
    inv = 255 - colour
    return inv


def deg_to_cm(degs, d):
    return 2 * d * np.tan(degs/2.0)

def cm_to_deg(cms, d):
    return 2 * np.arctan(cms/(2.0*d))

def find_ppi(pix_h, pix_v, diagonal):
    return np.sqrt(pix_h**2 + pix_v**2) / diagonal


def find_flicker_fs(frames, monitor_fs):
    return monitor_fs / float(frames)

def find_frames_in_cycle(flicker_fs, monitor_fs):
    return monitor_fs / float(flicker_fs)


def FFT(image):
	img = Image.open(image)
	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)
	mag = 20 * np.log(np.abs(fshift))
	
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	ax1.imshow(img)
	ax1.set_title('Image')
	ax2 = fig.add_subplot(122)
	ax2.imshow(mag, cmap = 'gray')
	ax2.set_title('Magnitude spectrum')
	
	plt.show()
	
	
class MyImage(object):
	
	def __init__(self, path):
	
		self.path = os.path.abspath(path)
		self.img = np.array(Image.open(self.path))
		
		
	def identify_global_local(self):
	
		path, name = os.path.split(self.path)
		name, ext = os.path.splitext(name)
		
		assert len(name) == 2, 'Image name should be 2 characters'
		
		self.global_ch = name[0].upper()
		self.local_ch = name[1].upper()
		

	def apply_colours(self, bg_col, fg_col):
	
		fg = self.img[:, :, 0] == 0
		
		self.img[fg] = fg_col
		self.img[~fg] = bg_col	
		
	def save(self, path):
		img = Image.fromarray(self.img)
		img.save(path)