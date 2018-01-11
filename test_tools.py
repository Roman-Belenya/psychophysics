import unittest
from experiment_part import *
from tools import *

class TestTools(unittest.TestCase):

    def test_get_fg_mask(self):
        image = np.random.choice(glob.glob('./images/line_drawings/*.png'))
        mask = get_fg_mask(image)

        self.assertTrue(-1 <= np.all(mask) <= 1)
        self.assertTrue(len(np.unique(mask)) == 2)

    def test_from_rgb(self):
        self.assertEqual(from_rgb(255), 1)
        self.assertEqual(from_rgb(0), -1)
        self.assertAlmostEqual(from_rgb(128), 0, places = 2)
        v = from_rgb(np.array([0, 0, 0]))
        self.assertTrue(np.all(v == [-1, -1, -1]))
        with self.assertRaises(Exception):
            from_rgb(-1)

    def test_to_rgb(self):
        self.assertEqual(to_rgb(-1), 0)
        self.assertEqual(to_rgb(1), 255)
        self.assertEqual(to_rgb(0), 127)
        with self.assertRaises(Exception):
            to_rgb(255)

    def test_change_colour(self):
        self.assertEqual(change_colour(130, -10), 120)
        c = np.array([100, 100, 100]); d = np.array([-10, 10, 0])
        self.assertTrue(np.all(change_colour(c, d) == [90, 110, 100]))
        c = np.array([255, 255, 255])
        self.assertTrue(np.all(change_colour(c, d) == c))

    def test_invert(self):
        self.assertTrue(np.all(invert([90, 110, 100]) == [165, 145, 155]))
        self.assertTrue(np.all(invert([0, 0, 0]) == [255, 255, 255]))

    def test_deg_to_cm(self):
        self.assertEqual(deg_to_cm(np.radians(0), 40), 0)
        s = np.radians(100)
        d = 40
        v = 2 * d * np.tan(s/2.0)
        self.assertEqual(deg_to_cm(s,d), v)



if __name__ == '__main__':
    unittest.main()
