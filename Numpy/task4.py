import numpy as np

def print_array(array, message=""):
    if message:
        print(message)
    print(array)
    print()

# Generate an array 10x10 
arr = np.random.randint(1, 100, size=(10, 10))
print_array(arr, "Initial 10x10 Array:")

# Save: text, CSV, .npy
def save_array(array, filename_base):
    np.savetxt(f"{filename_base}.txt", array, fmt='%d')
    np.savetxt(f"{filename_base}.csv", array, delimiter=',', fmt='%d')
    np.save(f"{filename_base}.npy", array)

# Load: text, CSV, .npy
def load_array(filename_base):
    array_txt = np.loadtxt(f"{filename_base}.txt", dtype=int)
    array_csv = np.loadtxt(f"{filename_base}.csv", delimiter=',', dtype=int)
    array_npy = np.load(f"{filename_base}.npy")
    return array_txt, array_csv, array_npy

# Summation 
def array_sum(array):
    return np.sum(array)

# Mean 
def array_mean(array):
    return np.mean(array)

# Median 
def array_median(array):
    return np.median(array)

# Standard Deviation 
def array_std(array):
    return np.std(array)

# Axis-Based Aggregate 
def axis_sum(array, axis):
    return np.sum(array, axis=axis)

def axis_mean(array, axis):
    return np.mean(array, axis=axis)

def axis_median(array, axis):
    return np.median(array, axis=axis)

def axis_std(array, axis):
    return np.std(array, axis=axis)

# Array Creation and Saving
save_array(arr, "initial_array")

# Loading and Verification
array_txt, array_csv, array_npy = load_array("initial_array")

print_array(array_txt, "Loaded Array from Text File:")
print_array(array_csv, "Loaded Array from CSV File:")
print_array(array_npy, "Loaded Array from NPY File:")

# Aggregate Computation and Reporting
sum_value = array_sum(arr)
mean_value = array_mean(arr)
median_value = array_median(arr)
std_value = array_std(arr)

print_array(sum_value, "Sum of All Elements:")
print_array(mean_value, "Mean of All Elements:")
print_array(median_value, "Median of All Elements:")
print_array(std_value, "Standard Deviation of All Elements:")

row_sum = axis_sum(arr, axis=1)
col_sum = axis_sum(arr, axis=0)
row_mean = axis_mean(arr, axis=1)
col_mean = axis_mean(arr, axis=0)
row_median = axis_median(arr, axis=1)
col_median = axis_median(arr, axis=0)
row_std = axis_std(arr, axis=1)
col_std = axis_std(arr, axis=0)

print_array(row_sum, "Row-wise Sum:")
print_array(col_sum, "Column-wise Sum:")
print_array(row_mean, "Row-wise Mean:")
print_array(col_mean, "Column-wise Mean:")
print_array(row_median, "Row-wise Median:")
print_array(col_median, "Column-wise Median:")
print_array(row_std, "Row-wise Standard Deviation:")
print_array(col_std, "Column-wise Standard Deviation:")

# Verification

# Verify that loaded arrays match the original array
assert np.array_equal(arr, array_txt), "Loaded array from text file does not match the original."
assert np.array_equal(arr, array_csv), "Loaded array from CSV file does not match the original."
assert np.array_equal(arr, array_npy), "Loaded array from NPY file does not match the original."

# Verify the dimensions and integrity of the original array
assert arr.shape == (10, 10), "The original array should be 10x10."

# Verify aggregate function results
assert sum_value == np.sum(arr), "Sum computation is incorrect."
assert mean_value == np.mean(arr), "Mean computation is incorrect."
assert median_value == np.median(arr), "Median computation is incorrect."
assert std_value == np.std(arr), "Standard deviation computation is incorrect."
