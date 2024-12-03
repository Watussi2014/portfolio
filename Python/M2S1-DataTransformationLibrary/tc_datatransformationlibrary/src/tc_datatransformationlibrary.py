import numpy as np


def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transpose the axis of the given matrix.

    Eg.
    transpose2d([[[1,2,3],[4,5,6]]])
    >> [[1,4],[2,5],[3,6]]
    """

    num_col = len(input_matrix[0])
    out_matrix = []
    in_matrix = []
    i = 0

    # Check if the shape of the matrix is correct
    for rows in input_matrix:
        if len(rows) != num_col:
            raise ValueError("Number of columns in rows not matching")

    while i <= num_col - 1:
        in_matrix = [row[i] for row in input_matrix]
        out_matrix.append(in_matrix)
        in_matrix = []
        i += 1

    return out_matrix


def window1d(
    input_array: list | np.ndarray,
    size: int,
    shift: int = 1,
    stride: int = 1,
    drop_remainder: bool = True,
) -> list[list | np.ndarray]:
    """
    Returns a list which contains subsets or windows of size s from a given a given 1-D array.

    Args:
        input_array: A 1-D array.
        size: The desired size of the windows.
        shift: The number of input element to shift between the start of each window.
        stride: The stride between input elements in a window.
        drop_remainder: Drop the windows that doesn't match the size.

    Eg.
        window1d([0,1,2,3,4,5], size=3)
        >> [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]

        window1d([0,1,2,3,4,5], size=3, stride=2, drop_remainder=True)
        >> [[0, 2, 4], [1, 3, 5]]

    """

    start = 0
    end = size
    output = []

    while start < len(input_array):
        window = []
        i = start
        while len(window) < size:
            try:
                window.append(input_array[i])
                i += stride
            except IndexError:
                break
        output.append(window)
        end += shift
        start += shift

    if drop_remainder:
        output = [list for list in output if len(list) == size]
        return output
    else:
        return output


def convolution2d(
    input_matrix: np.ndarray, 
    kernel: np.ndarray, 
    stride: int = 1
) -> np.ndarray:
    """
    Takes two 2-D array, an input matrix and a kernel and apply a cross-correlation operation with both.

    Eg.
    input_matrix = [[0,1,2],
                    [3,4,5],
                    [6,7,8]]
    kernel = [[0,1],
              [2,3]]

    convolution2d(input_matrix, kernel)
    >>[[19. ,25.]
      [37. ,43.]]
    """

    k_height, k_width = kernel.shape
    inp_height, inp_width = input_matrix.shape
    stride_width = 0
    stride_height = 0

    output = np.zeros(shape=(inp_height - k_height + 1, inp_width - k_width + 1))

    for i in range(output.shape[0]):
        stride_width = 0
        for j in range(output.shape[1]):
            sub_width = k_width + stride_width
            sub_height = k_height + stride_height

            sub_matrix = input_matrix[stride_height:sub_height, stride_width:sub_width]

            try:
                result = sum(
                    [
                        sub_matrix[k][l] * kernel[k][l]
                        for k in range(kernel.shape[0])
                        for l in range(kernel.shape[1])
                    ]
                )
            except IndexError as i:
                raise ValueError(
                    "Stride is to big, kernel sliding over the input matrix"
                )

            output[i][j] = result
            stride_width += stride
        stride_height += stride
    return output
