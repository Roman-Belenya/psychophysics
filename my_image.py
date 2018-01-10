from PIL import Image
import numpy as np
import os

class MyImage(object):

    def __init__(self, template_path, out_dir):
        '''template_path is binary template, out_dir is subject dir'''

        self.template_path = os.path.abspath(template_path)
        out_dir = os.path.abspath(out_dir)

        _, name = os.path.split(self.template_path)
        self.name, ext = os.path.splitext(name)

        self.parvo_path = os.path.join(out_dir, self.name + '_parvo' + ext)
        self.magno_path = os.path.join(out_dir, self.name + '_magno' + ext)
        self.unbiased_path = os.path.join(out_dir, self.name + '_unbiased' + ext)

        assert len(self.name) == 2, 'Image name should be 2 characters'

        self.global_letter = self.name[0].lower()
        self.local_letter = self.name[1].lower()
        
    def get_response_type(self, letter):
        letter = letter.lower()
        if letter == self.global_letter:
            return 'global'
        elif letter == self.local_letter:
            return 'local'


    def apply_colours(self, fg_col, bg_col, fg_grey, bg_grey):

        img = np.array(Image.open(self.template_path))
        fg = img[:, :, 0] == 0

        img[fg] = fg_col
        img[~fg] = bg_col
        image = Image.fromarray(img)
        image.save(self.parvo_path)

        img[fg] = fg_grey
        img[~fg] = bg_grey
        image = Image.fromarray(img)
        image.save(self.magno_path)

        img[fg] = [0]*3
        # img[~fg] = bg_grey
        image = Image.fromarray(img)
        image.save(self.unbiased_path)
