from PIL import Image
import numpy as np
from psychopy import monitors
import matplotlib.pyplot as plt
import os
import time


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
    if np.any(value < 0) or np.any(value > 255):
        raise Exception('Invalid input rgb value')

    return value / 127.5 - 1


def to_rgb(value):
    if value < -1 or value > 1:
        raise Exception('Invalid input value: should be -1 to 1')

    v = 255 + np.around((value - 1) * 127.5)
    return int(v)


def change_colour(colour, by):

    new_colour = colour + by
    if np.any(new_colour < 0) or np.any(new_colour > 255):
        return colour

    return new_colour

def invert(colour):
    if not isinstance(colour, np.ndarray):
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





