import numpy as np
import os
import nibabel as nib

from definitions import root_dir
from numpy.testing import assert_array_almost_equal

from nose.tools import assert_equals, assert_raises, assert_almost_equals
from numpy.testing import assert_array_equal, assert_almost_equal


''' Test measurements.distances.py'''
from labels_manager.tools.measurements.distances import lncc_distance


def test_simple_patches_values_lncc():

    patch1 = np.array([1, 2, 3])
    patch2 = np.array([1, 2, 3])

    assert lncc_distance(patch1, patch2) == 1.0

    patch1 = np.array([1, 2, 3])
    patch2 = np.array([0, 0, 0])

    assert lncc_distance(patch1, patch2) == 0.0

    patch1 = np.array([0, 0, 0])
    patch2 = np.array([1, 2, 3])

    assert lncc_distance(patch1, patch2) == 0.0

    patch1 = np.array([1, 0, 0])
    patch2 = np.array([0, 1, 0])

    assert lncc_distance(patch1, patch2) == 0.0


''' Test measurements.linear.py'''
from labels_manager.tools.measurements.linear import box_sides


def test_box_sides():
    test_image = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 1, 1, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]])

    expected_horizontal_ones = 4
    expected_vertical_ones = 7

    assert_array_equal(box_sides(test_image),
                       [expected_vertical_ones, expected_horizontal_ones])


''' Test measurements.linear.py'''
from labels_manager.tools.measurements.volumetric import centroid


def test_simple_centroid():

    test_image = np.array([[[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],

                           [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]])

    ans = centroid(test_image, labels=[1,2])
    assert_array_equal(ans[0], np.array([ 0.5  ,  2.625,  3.875]))
    assert_array_equal(ans[1], np.array([0.5, 5.5, 2.5]))

