import unittest
from experiment_part import *
from my_image import *
from tools import *
import json
import logging
import time

logger = logging.getLogger(__name__)

class TestExperimentPart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        with open('./parameters.json', 'rb') as f:
            cls.params = json.load(f)
        _id = '__test__'
        # os.makedirs('./__test__/stimuli')

        mon = load_monitor(cls.params['Monitors'][cls.params['current_monitor']])
        cls.win = visual.Window(
            size = mon.getSizePix(),
            monitor = mon,
            screen = 0,
            allowGUI = False,
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        cls.win.recordFrameIntervals = True

        cls.contrast = ContrastDetection(cls.win, _id, cls.params['default_colours'], cls.params['ContrastDetection'])
        cls.isolum = IsoluminanceDetection(cls.win, _id, cls.params['default_colours'], cls.params['IsoluminanceDetection'])
        cls.choice = FreeChoiceExperiment(cls.win, _id, cls.params['default_colours'], cls.params['FreeChoiceExperiment'])
        cls.divided = DividedAttentionExperiment(cls.win, _id, cls.params['default_colours'], cls.params['DividedAttentionExperiment'])
        cls.selective = SelectiveAttentionExperiment(cls.win, _id, cls.params['default_colours'], cls.params['SelectiveAttentionExperiment'])
        cls.stream_handler = logging.StreamHandler()
        logger.addHandler(cls.stream_handler)

    @classmethod
    def tearDownClass(cls):
        cls.win.winHandle.minimize()
        cls.win.close()
        # shutil.rmtree('./__test__/')
        logger.removeHandler(cls.stream_handler)

    def test_files(self):
        self.assertTrue(os.path.isfile('./parameters.json'))
        self.assertTrue(os.path.isdir(self.contrast.images_dir))
        self.assertTrue(os.path.isdir(self.isolum.images_dir))
        self.assertTrue(os.path.isdir(self.choice.images_dir))

        imgs = glob.glob(self.contrast.images_dir + '/*.png')
        self.assertGreater(len(imgs), self.contrast.n_trials, 'Not enough images: {}'.format(len(imgs)))

        imgs = glob.glob(self.isolum.images_dir + '/*.png')
        n_isolum = self.isolum.n_trials * (len(self.isolum.blocks_seq) / 2.0)
        self.assertGreater(len(imgs), n_isolum, 'Not enough images :{}'.format(len(imgs)))

        imgs = glob.glob(self.choice.images_dir + '/*.png')
        self.assertEqual(len(imgs), 6)

        imgs = glob.glob(self.divided.images_dir + '/*.png')
        self.assertEqual(len(imgs), 6)

    def test_seq_files(self):
        for exp in [self.choice, self.divided]:
            file = exp.seq_file
            self.assertTrue(os.path.isfile(file))
            stims = [os.path.split(i)[1] for i in exp.images]
            stims = [i.split('.png')[0] for i in stims]

            with open(file, 'rb') as f:
                reader = csv.reader(f)
                for cond, stim in reader:
                    self.assertIn(cond, ['magno', 'parvo', 'unbiased'], 'Incorrect condition name in seq_file: {}'.format(cond))
                    self.assertIn(stim, stims, 'Incorrect stim name in seq_file: {}'.format(stim))


    def test_frame_rate(self):
        mon_fs = self.win.monitor.refresh_rate
        self.win.refreshThreshold = 1./mon_fs + 0.004
        framerate = self.win.getActualFrameRate(nIdentical = 20,
            nMaxFrames = 200,
            nWarmUpFrames = 100,
            threshold = 1)
        self.assertEqual(mon_fs, round(framerate), 'Incorrect monitor frame rate: {}, actual is {}'.format(mon_fs, framerate))
        logger.info('actual framerate is {}'.format(framerate))




    def test_timing(self):
        self.win.nDroppedFrames = 0
        frame = 0
        t = 10
        stim = visual.TextStim(win = self.win, text = '0', pos = (0,0))
        t0 = time.time()
        while frame < self.win.monitor.refresh_rate * t:
            if frame % 4 == 0:
                stim.text = '{:.2f}'.format(t - float(frame) / self.win.monitor.refresh_rate)
            stim.draw()
            self.win.flip()
            frame += 1
        dt = time.time() - t0

        logger.info('dropped {} frames: {}%'.format(self.win.nDroppedFrames, self.win.nDroppedFrames*100.0/frame))
        logger.info('timing error is {}'.format(dt - t))
        self.assertAlmostEqual(dt, t, delta = 0.5, msg = 'Large timing error: {}, should be {} sec'.format(dt, t))


    def test_flicker(self):
        self.win.nDroppedFrames = 0
        img = os.path.join('.', 'images', 'circle.png')
        fg = get_fg_mask(img)
        self.isolum.stim.mask = fg
        self.isolum.col_delta = np.array([0, 1, 0])
        colour = self.params['default_colours']['bg_col']
        half_cycle = self.win.monitor.refresh_rate / (2.0 * self.isolum.flicker_fs)
        frame = 0
        n = 0
        t = 10

        while frame < self.win.monitor.refresh_rate * t:
            if frame % half_cycle == 0:
                if all(self.isolum.stim.color == self.isolum.fix_col):
                    self.isolum.stim.color = colour
                    n += 1
                else:
                    self.isolum.stim.color = self.isolum.fix_col
            self.isolum.stim.draw()
            self.win.flip()
            frame += 1

            ans = event.getKeys(keyList = ['up', 'down', 'return'])
            if ans:
                if ans[0] == 'up':
                    colour = change_colour(colour, self.isolum.col_delta)
                elif ans[0] == 'down':
                    colour = change_colour(colour, -1*self.isolum.col_delta)
                elif ans[0] == 'return':
                    logger.info('Colours are {} and {}'.format(colour, self.isolum.fix_col))

        cycles_per_sec = float(n) / (float(frame) / self.win.monitor.refresh_rate)
        msperframe = 1000. / self.win.monitor.refresh_rate
        fints = np.array(self.win.frameIntervals) * 1000
        t1 = fints.mean() - fints.std()
        t2 = fints.mean() + fints.std()

        logger.info('Flicker frequency is {}'.format(cycles_per_sec))
        logger.info('dropped {} frames: {}%'.format(self.win.nDroppedFrames, self.win.nDroppedFrames*100.0/frame))
        logger.info('{} +- {} ms to refresh each frame, should be {}'.format(fints.mean(), fints.std(), msperframe))

        self.assertTrue(t1 < msperframe < t2, 'Strange refresh period ({}, should be {})'.format(fints.mean(), msperframe))
        self.assertEqual(self.isolum.flicker_fs, cycles_per_sec, 'Strange flicker rate: set to {}, but actually is {}'.format(self.isolum.flicker_fs, cycles_per_sec))
        self.assertLessEqual(2.0 * self.isolum.flicker_fs, self.win.monitor.refresh_rate, 'Flicker frequency cannot be greater than half the monitor fs: set to {}'.format(self.isolum.flicker_fs))
        self.assertLess(self.win.nDroppedFrames, frame*0.05, msg = 'Too many dropped frames ({})'.format(self.win.nDroppedFrames))


    def test_gamma(self):
        self.win.nDroppedFrames = 0
        t = 5.0
        width_pix = self.win.size[0]
        bg = visual.GratingStim(win = self.win, tex = None, size = self.win.size, color = 0, colorSpace = 'rgb255', units = 'pix')
        stim = visual.GratingStim(win = self.win, tex = None, size = 200, color = 1, colorSpace = 'rgb255', units = 'pix')#, pos = [-width_pix/2.0, 0])
        bg.draw()
        stim.draw()
        self.win.flip()
        clock = core.Clock()
        # pp = width_pix/(t * self.win.monitor.refresh_rate)
        while clock.getTime() < t:
            # stim.pos[0] += pp
            stim.ori += 360.0*5 / (t * self.win.monitor.refresh_rate)
            bg.draw()
            stim.draw()
            self.win.flip()

        logger.info('dropped {} frames: {}%'.format(self.win.nDroppedFrames, self.win.nDroppedFrames*100.0/(t*self.win.monitor.refresh_rate)))


    def test_warm_up(self):

        stim = visual.GratingStim(win = self.win, size = 1024, units = 'pix')
        clock = core.Clock()
        while clock.getTime() < 10:
            stim.tex = np.random.rand(1024, 1024) * 2 - 1
            stim.draw()
            self.win.flip()






if __name__ == '__main__':
    unittest.main()
