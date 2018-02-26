from psychopy import tools
import numpy as np

def dklCart2dkl(dklCart):

    z,y,x = dklCart

    radius = np.sqrt(x**2 + y**2 + z**2)
    azimuth = np.arctan2(x, y)
    if azimuth < 0:
        azimuth += 2 * np.pi
    azimuth *= (180 / np.pi)
    elevation = np.arctan(float(z) / np.sqrt(x**2 + y**2)) * (180 / np.pi)
    # elevation = np.arcsin(z/radius)

    return np.array([elevation, azimuth, radius])


def dkl2rgb(dkl, dkl2rgb_m):
    rgb = tools.colorspacetools.dkl2rgb(dkl, dkl2rgb_m)
    return (rgb + 1) * 127.5

def lms2rgb(lms, lms2rgb_m):
    rgb = tools.colorspacetools.lms2rgb(lms, lms2rgb_m)
    return (rgb + 1) * 127.5

def rgb2dkl(rgb, rgb2dkl_m):
    rgb = rgb / 127.5 - 1
    dkl = np.dot(rgb2dkl_m, rgb)
    return dklCart2dkl(dkl)

def rgb2lms(rgb, rgb2lms_m):
    rgb = rgb / 127.5 - 1
    lms = tools.colorspacetools.rgb2lms(rgb, rgb2lms_m)
    return lms
