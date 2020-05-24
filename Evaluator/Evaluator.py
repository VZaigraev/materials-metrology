from skimage.feature import blob_log
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

def evaluateLOGbatch(grayImages):
    result = []
    for i in range(len(grayImages)):
        result.append(evaluateLOG(grayImages[i]))
    return result