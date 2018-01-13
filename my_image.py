from PIL import Image
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

class MyImage(object):

    def __init__(self, template_path, out_dir, cond, colours_dict, make_img = True):
        '''template_path is b&w template, out_dir is subject dir'''

        self.template_path = os.path.abspath(template_path)
        out_dir = os.path.abspath(out_dir)
        self.cond = cond

        _, name = os.path.split(self.template_path)
        self.name, ext = os.path.splitext(name)

        self.stim_path = os.path.join(out_dir, self.name + '_' + cond + ext)
        # e.g. './P01/stimuli_free_choice/Hs_parvo.png'

        if make_img and not os.path.isfile(self.stim_path):

            if cond == 'magno':
                fg = colours_dict['fg_grey']
                bg = colours_dict['bg_grey']
            elif cond == 'parvo':
                fg = colours_dict['fg_col']
                bg = colours_dict['bg_col']
            elif cond == 'unbiased':
                fg = [0,0,0]
                bg = colours_dict['bg_grey']

            self.make_image(self.stim_path, fg = fg, bg = bg)

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


    def make_image(self, path, fg, bg):

        # img = np.array(Image.open(self.template_path))
        img = np.array(Image.open(self.template_path))
        fg_mask = img[:, :, 0] == 0

        img[fg_mask] = fg
        img[~fg_mask] = bg

        Image.fromarray(img).save(path)
        logger.info('created image: {}'.format(path))

