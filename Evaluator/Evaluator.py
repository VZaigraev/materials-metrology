from skimage.feature import blob_log, blob_dog, blob_doh
from math import sqrt
import numpy as np
from skimage.filters import gaussian

# Laplassian of Gaussian
def evaluateLOG(grayImage):
    log = blob_log(grayImage, max_sigma=30, num_sigma=15, threshold=.1)
    log[:, 2] = log[:, 2] * sqrt(2)
    coordinates = np.empty((log.shape[0], 5))
    coordinates[:, 4] = 1
    coordinates[:, 0] = log[:, 1] - log[:, 2]
    coordinates[:, 1] = log[:, 0] - log[:, 2]
    coordinates[:, 2] = log[:, 1] + log[:, 2]
    coordinates[:, 3] = log[:, 0] + log[:, 2]
    return coordinates

# Difference of Gaussian
def evaluateDOG(grayImage):
    log = blob_dog(grayImage, max_sigma=30, threshold=.1)
    log[:, 2] = log[:, 2] * sqrt(2)
    coordinates = np.empty((log.shape[0], 5))
    coordinates[:, 4] = 1
    coordinates[:, 0] = log[:, 1] - log[:, 2]
    coordinates[:, 1] = log[:, 0] - log[:, 2]
    coordinates[:, 2] = log[:, 1] + log[:, 2]
    coordinates[:, 3] = log[:, 0] + log[:, 2]
    return coordinates

# Determinant of Hessian
def evaluateDOH(grayImage):
    log = blob_doh(grayImage, max_sigma=30, threshold=.01)
    #log[:, 2] = log[:, 2] * sqrt(2)
    coordinates = np.empty((log.shape[0], 5))
    coordinates[:, 4] = 1
    coordinates[:, 0] = log[:, 1] - log[:, 2]
    coordinates[:, 1] = log[:, 0] - log[:, 2]
    coordinates[:, 2] = log[:, 1] + log[:, 2]
    coordinates[:, 3] = log[:, 0] + log[:, 2]
    return coordinates



def evaluatebatch(grayImages, f):
    result = []
    for i in range(len(grayImages)):
        result.append(f(grayImages[i]))
    return result
