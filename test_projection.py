import tempfile
import unittest
from pathlib import Path

import numpy as np

from Ex0 import create_projection, read_planes


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.volume = np.arange(20 * 20 * 20, dtype=np.uint16).reshape(20, 20, 20)

    def test_triangle_valid_and_voxel_value(self):
        pts = np.array([[1, 1, 1], [5, 1, 1], [1, 5, 1]], dtype=float)
        out = create_projection(self.volume, pts)
        self.assertEqual(out.shape, (5, 7))
        self.assertEqual(out[0, 3], self.volume[1, 1, 1])

    def test_trapezoid(self):
        pts = np.array([[2, 2, 1], [2, 4, 1], [8, 1, 1], [8, 5, 1]], dtype=float)
        out = create_projection(self.volume, pts)
        self.assertEqual(out.shape, (7, 5))

    def test_reject_invalid_triangle(self):
        with self.assertRaises(ValueError):
            create_projection(self.volume, np.array([[1, 1, 1], [5, 1, 1], [1, 3, 1]], float))

    def test_reject_non_coplanar_trapezoid(self):
        points = np.array([[1, 1, 1], [1, 3, 1], [5, 1, 1], [5, 3, 2]], float)
        with self.assertRaises(ValueError):
            create_projection(self.volume, points)

    def test_outside_samples_are_zero(self):
        points = np.array([[-2, 2, 1], [2, 2, 1], [-2, 6, 1]], float)
        image = create_projection(self.volume, points)
        self.assertTrue((image == 0).any())

    def test_csv_three_and_four_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planes.csv"
            path.write_text('1,1,1,5,1,1,1,5,1\n2,2,1,2,4,1,8,1,1,8,5,1\n')
            planes = read_planes(path)
            self.assertEqual([len(p) for p in planes], [3, 4])

    def test_csv_invalid_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text('1,2,3\n')
            with self.assertRaisesRegex(ValueError, 'line 1'):
                read_planes(path)


if __name__ == '__main__':
    unittest.main()
