import numpy as np
from scipy import stats


def get_threshold(like_array):
    arr = np.array(like_array)
    mean = stats.trim_mean(arr, 0.1)
    return mean
