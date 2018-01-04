import unittest
from experiment_part import *
from my_image import *
from tools import *
import json

class TestExperimentPart(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        
        with open('./parameters.json', 'rb') as f:
            self.params = json.load(f)
        id = '__test__'
        os.makedirs('./__test__/stimuli')
        self.win = visual.Window(
            size = [1920, 1080],
            monitor = 'labBENQ',
            fullscr = True,
            colorSpace = 'rgb255',
            color = 128,
            units = 'deg')
        self.contrast = ContrastDetection(self.win, id, self.params['ContrastDetection'])
        self.isolum = IsoluminanceDetection(self.win, id, self.params['IsoluminanceDetection'])
        self.free = FreeChoiceExperiment(self.win, id, self.params['FreeChoiceExperiment'])
        
    @classmethod    
    def tearDownClass(self):
        self.win.close()
        shutil.rmtree('./__test__/')
        
    def test_files(self):
        self.assertTrue(os.path.isfile('./parameters.json'))
        self.assertTrue(os.path.isdir('./images/letters'))
        self.assertTrue(os.path.isdir('./images/line_drawings'))
        
        
    def test_refresh_rate(self):
        mon_fs = self.params['IsoluminanceDetection']['monitor_fs']
        self.win.refreshThreshold = 1./mon_fs + 0.004
        framerate = self.win.getActualFrameRate(nIdentical = 20, 
            nMaxFrames = 200, 
            nWarmUpFrames = 100, 
            threshold = 1)
        self.assertEqual(mon_fs, round(framerate))
        
     
    def test_iso_colours(self):
        self.win.recordFrameIntervals = True
        img = os.path.join('.', 'images', 'circle.png')
        fg = get_fg_mask(img)
        self.isolum.stim.mask = fg
        self.isolum.col_delta = np.array([0, 1, 0])
        col = self.isolum.run_trial([0, 120, 0])
        
        fint = 1000. / self.params['IsoluminanceDetection']['monitor_fs']
        fints_ms = np.array(self.win.frameIntervals) * 1000
        self.assertTrue( np.all(fints_ms < fint+1) , 'Too long refresh period')
        self.assertLess(self.win.nDroppedFrames, 5, 'Too many dropped frames')
        
    def test_image_creation(self):
        out_dir = './__test__/stimuli'
        for img in self.free.images:
            image = MyImage(img, out_dir)
            image.apply_colours(100, 200, np.array([255, 255, 0]), np.array([0, 0, 255]))
        
        

        
if __name__ == '__main__':
    unittest.main()