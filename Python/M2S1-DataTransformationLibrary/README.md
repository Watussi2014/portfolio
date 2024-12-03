# Description

Python library for the Data Engineering course at Turing College.

The library provide 3 functions:

* transpose2d : Switch the axis of a 2d matrix.
* windows1d : Create windows from a 1d array.
* convolution2d: Apply a cross-correlation operation to a 2d array.


# Quick documentation

**transpose2d**

Transpose the axis of a 2-D matrix.




For example, a given 2x3 matrix will be returned as a 3x2 matrix.


The function signature is : transpose2d(input_matrix)

The function only take one argument, a list of list that will represent the matrix.



````
matrix = [[1,2,3],[4,5,6]]
transpose2d(matrix)
>> [[1,4],[2,5],[3,6]]
````


**window1d**

Returns a list which contains subsets or windows of size s from a given a given 1-D array.

The function signature is : window1d(input_array, size, shift=1, stride=1, drop_remainder=True)

* input_array : A list or numpy array
* size : integer. The desired size for the windows
* shift : integer. The number of input element to shift between the start of each window.
* stride : integer. The stride between input elements in a window.
* drop_remainder : bool. Drop the windows that doesn't match the size.

```
window1d([0,1,2,3,4,5], size=3)
>> [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
```


**convolution2d**

Takes two 2-D array, an input matrix and a kernel and apply a cross-correlation operation with both.

The function signature is : convolution2d(input_matrix, kernel, stride=1)

* input_matrix : list or np.ndarray.
* kernel : list or np.ndarray.
* stride : integer. The stride between the postions of the convulation windows.


````
input_matrix = [[0,1,2],
                [3,4,5],
                [6,7,8]]

kernel = [[0,1],
          [2,3]]
    
convolution2d(input_matrix, kernel)
>>[[19. ,25.]
   [37. ,43.]]
````

# Publishing

The goal of the project is also to practice publishing libraries to PyPI.




I have decided to upload this library to testPyPI because it's a small library.




It can be found [here](https://test.pypi.org/project/tc_datatransformationlibrary/)


# Testing
Small tests are written in the tests folder and can be used using pytest.