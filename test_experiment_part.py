import unittest
from experiment_part import *
from my_image import *
from tools import *
import json
import logging

logger = logging.getLogger(__name__)

class TestExperimentPart(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        with open('./parameters.json', 'rb') as f:
            cls.params = json.load(f)
        id = '__test__'
        os.makedirs('./__test__/stimuli')
        cls.win = visual.Window(
            size = [1920, 1080],
            monitor = 'labBENQ',
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        cls.contrast = ContrastDetection(cls.win, id, cls.params['ContrastDetection'])
        cls.isolum = IsoluminanceDetection(cls.win, id, cls.params['IsoluminanceDetection'])
        cls.choice = FreeChoiceExperiment(cls.win, id, cls.params['FreeChoiceExperiment'])
        cls.stream_handler = logging.StreamHandler()
        logger.addHandler(cls.stream_handler)

    @classmethod
    def tearDownClass(cls):
        cls.win.close()
        shutil.rmtree('./__test__/')
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

    def test_seq_file(self):
        file = self.choice.seq_file
        self.assertTrue(os.path.isfile(file))
        stims = [os.path.split(i)[1] for i in self.choice.images]
        stims = [i.split('.png')[0] for i in stims]

        with open(file, 'rb') as f:
            reader = csv.reader(f)
            for cond, stim in reader:
                self.assertIn(cond, ['magno', 'parvo', 'unbiased'], 'Incorrect condition name in seq_file: {}'.format(cond))
                self.assertIn(stim, stims, 'Incorrect stim name in seq_file: {}'.format(stim))

    def test_viewing_distance(self):
        mon = monitors.Monitor(self.params['monitor_name'])
        self.assertEqual(self.params['viewing_distance'], mon.getDistance(), 'Need to update viewing distance')


    def test_frame_rate(self):
        mon_fs = self.isolum.monitor_fs
        self.win.refreshThreshold = 1./mon_fs + 0.004
        framerate = self.win.getActualFrameRate(nIdentical = 20,
            nMaxFrames = 200,
            nWarmUpFrames = 100,
            threshold = 1)
        self.assertEqual(mon_fs, round(framerate), 'Incorrect monitor frame rate: {}, actual is {}'.format(mon_fs, framerate))
        logger.info('actual framerate is {}'.format(framerate))

    def test_flicker_fs(self):
        mfs = self.isolum.monitor_fs
        ffs = self.isolum.flicker_fs
        self.assertLessEqual(2 * ffs, mfs, 'Flicker rate should be at least twice as little as monitor fs')

    def test_iso_colours(self):
        self.win.recordFrameIntervals = True
        img = os.path.join('.', 'images', 'circle.png')
        fg = get_fg_mask(img)
        self.isolum.stim.mask = fg
        self.isolum.col_delta = np.array([0, 1, 0])
        col = self.isolum.run_trial([0, 120, 0])

        msperframe = 1000. / self.isolum.monitor_fs
        fints = np.array(self.win.frameIntervals) * 1000
        t1 = fints.mean() - fints.std()
        t2 = fints.mean() + fints.std()
        self.assertTrue(t1 < msperframe < t2, 'Strange refresh period ({}, should be {})'.format(fints.mean(), msperframe))
        self.assertLess(self.win.nDroppedFrames, 5, msg = 'Too many dropped frames ({})'.format(self.win.nDroppedFrames))
        logger.info('it takes {} ms to refresh each frame'.format(msperframe))
        logger.info('dropped {} frames'.format(self.win.nDroppedFrames))

    def test_image_creation(self):
        out_dir = './__test__/stimuli'
        for img in self.choice.images:
            image = MyImage(img, out_dir)
            image.apply_colours(fg_col = np.array([255, 255, 0]),
                                bg_col = np.array([0, 0, 255]),
                                fg_grey = 128,
                                bg_grey = 131)
            self.assertTrue(os.path.isfile(image.parvo_path))
            self.assertTrue(os.path.isfile(image.magno_path))
            self.assertTrue(os.path.isfile(image.unbiased_path))




if __name__ == '__main__':
    unittest.main()
