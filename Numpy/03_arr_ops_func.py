import numpy as np

def print_array(array, message=""):
    if message:
        print(message)
    print(array)
    print()

# Generate an array 6x6
arr = np.random.randint(1, 100, size=(6, 6))
print_array(arr, "Initial 6x6 Array:")

# Transpose 
def transpose_array(array):
    return array.T

# Reshape 
def reshape_array(array, new_shape):
    return array.reshape(new_shape)

# Split 
def split_array(array, sections, axis=0):
    return np.array_split(array, sections, axis)

# Combine 
def combine_arrays(*arrays):
    return np.concatenate(arrays, axis=0)

# Transpose the array
transposed_array = transpose_array(arr)
print_array(transposed_array, "Transposed Array:")

# Reshape the array from 6x6 to 3x12
reshaped_array = reshape_array(arr, (3, 12))
print_array(reshaped_array, "Reshaped Array (6x6 to 3x12):")

# Split the array into 2 sub-arrays along axis 0
split_arrays = split_array(arr, 2, axis=0)
for i, split_arr in enumerate(split_arrays):
    print_array(split_arr, f"Split Array {i + 1}:")

# Combine the split arrays back into one
combined_array = combine_arrays(*split_arrays)
print_array(combined_array, "Combined Array:")

# Verification
# Ensure the transposed array has the correct shape
assert transposed_array.shape == (6, 6), "Transposed array shape should be (6, 6)."

# Ensure the reshaped array has the correct shape
assert reshaped_array.shape == (3, 12), "Reshaped array shape should be (3, 12)."

# Ensure the combined array has the same shape as the original
assert combined_array.shape == arr.shape, "Combined array should have the same shape as the original array."
