from tc_datatransformationlibrary import transpose2d, window1d, convolution2d
import numpy as np

def test_transpose():
    assert transpose2d([[1,2,3],[4,5,6]]) == [[1,4],[2,5],[3,6]]
    assert transpose2d([[1,2,3],[4,5,6],[7,8,9]]) == [[1,4,7],[2,5,8],[3,6,9]]
    assert transpose2d([[1,2,3]]) == [[1],[2],[3]]
    assert transpose2d([[1],[2],[3]]) == [[1,2,3]]

def test_window():
    assert window1d([0,1,2,3,4,5], size=3) == [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
    assert window1d([0,1,2,3,4,5], size=3, stride=2) == [[0, 2, 4], [1, 3, 5]]
    assert window1d([0,1,2,3,4,5,6,7,8], size=4, shift=2, drop_remainder=False) == [[0,1,2,3],[2,3,4,5],[4,5,6,7],[6,7,8],[8]]

def test_convolution():
    convolution2d(np.array([[0,1,2],[3,4,5],[6,7,8]]), np.array([[0,1],[2,3]])) == [[19. ,25.],[37. ,43.]] 
    convolution2d(np.array([[0,1,2],[3,4,5],[6,7,8]]), np.array([[0,0],[0,0]])) == [[0. ,0.],[0. ,0.]]
    convolution2d(np.array([[0,1],[2,3]]), np.array([[0,1],[2,3]])) == [[14]]