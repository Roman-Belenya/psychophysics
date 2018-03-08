import colour_spaces as col
import numpy as np

cr = col.ColourRepresentations()

rgb = np.array([255,255,255])
lms = cr.rgb2lms(rgb)
dkl_cart = cr.lms2dkl(lms)
dkl = cr.dkl_cart2sph(dkl_cart)

dkl_cart1 = cr.dkl_sph2cart(dkl)
lms1 = cr.dkl2lms(dkl_cart1)
rgb1 = cr.lms2rgb(lms1)

print np.array([rgb, rgb1])
print
print np.array([lms, lms1])
print
print np.array([dkl_cart, dkl_cart1])
print
print dkl
print
print

rgb = np.array([0,0,0])
lms = cr.rgb2lms(rgb)
dkl_cart = cr.lms2dkl(lms)
dkl = cr.dkl_cart2sph(dkl_cart)

dkl_cart1 = cr.dkl_sph2cart(dkl)
lms1 = cr.dkl2lms(dkl_cart1)
rgb1 = cr.lms2rgb(lms1)

print np.array([rgb, rgb1])
print
print np.array([lms, lms1])
print
print np.array([dkl_cart, dkl_cart1])
print
print dkl


print
rgb = np.array([128]*3)
lms = cr.rgb2lms(rgb)
dkl_cart = cr.lms2dkl(lms)
dkl = cr.dkl_cart2sph(dkl_cart)

dkl_cart1 = cr.dkl_sph2cart(dkl)
lms1 = cr.dkl2lms(dkl_cart1)
rgb1 = cr.lms2rgb(lms1)

print np.array([rgb, rgb1])
print
print np.array([lms, lms1])
print
print np.array([dkl_cart, dkl_cart1])
print
print dkl
