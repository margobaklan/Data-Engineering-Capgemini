import numpy as np

def print_array(array, message=""):
    if message:
        print(message)
    print(array)
    print()

# Create a one-dimensional array with values ranging from 1 to 10
arr1 = np.arange(1, 11)
print_array(arr1, "One-dimensional array:")

# Create a two-dimensional array 3x3 containing values from 1 to 9
arr2 = np.arange(1, 10).reshape(3, 3)
print_array(arr2, "Two-dimensional array:")

# Access and print the third element of the one-dimensional array
third_element = arr1[2]
print_array(third_element, "Third element of the one-dimensional array:")

# Slice and print the first two rows and columns of the two-dimensional array
sliced_array = arr2[:2, :2]
print_array(sliced_array, "First two rows and columns of the two-dimensional array:")

# Add 5 to each element of the one-dimensional array
added_array = arr1 + 5
print_array(added_array, "One-dimensional array after adding 5 to each element:")

# Multiply each element of the two-dimensional array by 2
multiplied_array = arr2 * 2
print_array(multiplied_array, "Two-dimensional array after multiplying each element by 2:")
