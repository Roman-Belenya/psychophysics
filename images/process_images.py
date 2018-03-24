from PIL import Image
import numpy as np
import glob
import os

path = os.path.abspath("C:\Users\marotta_admin\Desktop\BOSS\__Set of stimuli\Modified stimuli\Line drawings")
images = glob.glob(os.path.join(path, '*.jpg'))

for image in images:
    img = Image.open(image)

    arr = np.array(img)
    arr[arr > 128] = 255
    arr[arr <= 128] = 0

    if len(np.unique(arr)) != 2:
        print image

    img = Image.fromarray(arr)
    img.resize((1024, 1024), Image.NEAREST)

    img.save(image[:-3] + 'png')
