import numpy as np
from numpy.testing import assert_array_equal

from LABelsToolkit.tools.detections.island_detection import island_for_label


def test_island_for_label_ok_input():
    in_data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    expected_ans_False = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
                          [0, 3, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0],
                          [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                          [0, 5, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    expected_ans_True = [[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                         [0, -1,  0,  0,  0,  0,  0,  0, -1,  0,  0,  0],
                         [0, -1,  0,  0,  1,  1,  0,  0, -1,  0,  0,  0],
                         [0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0],
                         [0, -1,  0,  1,  0,  1,  0,  0,  0,  0,  0,  0],
                         [0,  0,  0,  1,  1,  1,  1,  0,  0,  0,  0,  0],
                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                         [0, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                         [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

    ans_False = island_for_label(in_data, 1, emphasis_max=False)

    ans_True = island_for_label(in_data, 1, emphasis_max=True)

    assert_array_equal(expected_ans_False, ans_False)
    assert_array_equal(expected_ans_True, ans_True)


def test_island_for_label_no_label_in_input():
    in_data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    bypassed_ans = island_for_label(in_data, 2, emphasis_max=False)
    assert_array_equal(bypassed_ans, in_data)
