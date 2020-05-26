from skimage.feature import blob_log, blob_dog, blob_doh, canny
from skimage.transform import hough_circle, hough_circle_peaks
from math import sqrt
import numpy as np
from skimage import img_as_ubyte
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

def evaluateHough(grayImage):
    byte_image = img_as_ubyte(grayImage)
    edges = canny(byte_image, sigma=2)
    hough_radii = np.arange(1, 100, 2)
    hough_res = hough_circle(edges, hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=200)
    log = np.array(list(zip(cy, cx, radii)))
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
