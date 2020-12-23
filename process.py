from Evaluator.Evaluator import evaluateLOG
import argparse
import cv2
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('--draw', type=bool, default=True, required=False)
    return parser


def load_image(path):
    img = cv2.imread(path)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return imgGray


def draw(src_img, pred, src_path):
    img = src_img.copy()
    dir = os.path.join(".", "result")
    path = os.path.join(dir, f"img-{os.path.basename(src_path)}.png")
    if not os.path.exists(dir):
        os.mkdir(dir)
    col_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for j in range(pred.shape[0]):
        cv2.rectangle(col_img, (int(pred[j, 0]), int(pred[j, 1])), (int(pred[j, 2]), int(pred[j, 3])),
                      (0, 0, 255), 2)
    cv2.imwrite(path, col_img)
    return path


def create_histogram(coordinates, src_path):
    dim1 = np.abs(coordinates[:, 0] - coordinates[:, 2])
    dim2 = np.abs(coordinates[:, 1] - coordinates[:, 3])
    areas = dim1 * dim2

    img_path = create_image_histogram(areas, src_path)
    text_path = create_text_histogram(areas, src_path)
    return img_path, text_path


def create_image_histogram(areas, src_path):
    dir = os.path.join(".", "result")
    path = os.path.join(dir, f"hist-{os.path.basename(src_path)}.png")
    if not os.path.exists(dir):
        os.mkdir(dir)

    plt.hist(areas, bins=10)
    plt.savefig(path)
    return path


def create_text_histogram(areas, src_path):
    dir = os.path.join(".", "result")
    path = os.path.join(dir, f"hist-{os.path.basename(src_path)}.csv")
    if not os.path.exists(dir):
        os.mkdir(dir)

    hist = np.histogram(areas, bins=10)
    row_names = [f"({int(hist[1][i])}-{int(hist[1][i+1])})" for i in range(hist[1].shape[0] - 1)]
    result = pd.DataFrame({"Interval": row_names, "Count": hist[0]})
    result.to_csv(path)
    return path


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    print("Loading")
    img = load_image(namespace.path)
    print(f"Loaded image")
    coordinates = evaluateLOG(img)
    print(f"Found {coordinates.shape[0]} particles")
    if namespace.draw:
        result_img_path = draw(img, coordinates, namespace.path)
        print(f"Saved result image: {result_img_path}")

    hist_img_path, hist_text_path = create_histogram(coordinates, namespace.path)
    print(f"Saved csv histogram: {hist_text_path}")
    print(f"Saved png histogram: {hist_img_path}")