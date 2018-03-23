from PIL import Image, ImageFilter
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

class MyImage(object):

    def __init__(self, template_path, cond, colours_dict):
        '''template_path is b&w template'''

        self.template_path = os.path.abspath(template_path)
        self.cond = cond

        _, name = os.path.split(self.template_path)
        self.name, ext = os.path.splitext(name)

        if cond == 'magno':
            self.fg = colours_dict['fg_grey']
            self.bg = colours_dict['bg_grey']
        elif cond == 'parvo':
            self.fg = colours_dict['fg_col']
            self.bg = colours_dict['bg_col']
        elif cond == 'unbiased':
            self.fg = [0,0,0]
            self.bg = colours_dict['bg_grey']

        self.global_letter = self.name[0].lower()
        self.local_letter = self.name[1].lower()


    def get_response_type(self, letter):

        letter = letter.lower()
        if letter == self.global_letter:
            return 'global'
        elif letter == self.local_letter:
            return 'local'


    def has_letter(self, letter):

        if letter.lower() in [self.global_letter, self.local_letter]:
            return True
        else:
            return False


    def is_congruent(self):

        if self.global_letter == self.local_letter:
            return True
        else:
            return False


    def make_image(self, blur = 1):

        arr = np.array(Image.open(self.template_path))
        fg_mask = arr[:, :, 0] == 0

        arr[fg_mask] = self.fg
        arr[~fg_mask] = self.bg

        img = Image.fromarray(arr)
        if blur:
            img = img.filter(ImageFilter.GaussianBlur(radius = blur))

        logger.info('created {} {} image'.format(self.cond, self.name))
        return img
