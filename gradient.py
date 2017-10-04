from PIL import Image, ImageDraw, ImageFont
import numpy as np

lw = 50

grad = np.zeros((520, 256 * lw, 3), np.uint8)

for i in range(256):
    grad[ :, i*lw:i*lw+lw, :] += i

img = Image.fromarray(grad)
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', lw/2)

d = ImageDraw.Draw(img)

for i in range(256):
    d.text((i*lw, i*2), str(i), font = fnt, fill = (255, 0, 0))

img.save('gradient.png', 'PNG', dpi = (300,300))

# img.show()
