import sys
import argparse
from Evaluator.Evaluator import evaluateLOGbatch
from Loader.Loader import load_csv, load_xml
from QualityProcessor.Processor import meanAveragePrecision
import cv2
from skimage.color import gray2rgb


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('type', type=str)
    parser.add_argument('draw', type=bool, default=False)
    return parser

def draw(img, truth, pred):
    for i in range(len(img)):
        col_img = cv2.cvtColor(img[i], cv2.COLOR_GRAY2BGR)

        for j in range(pred[i].shape[0]):
            cv2.rectangle(col_img, (int(pred[i][j, 0]), int(pred[i][j, 1])), (int(pred[i][j, 2]), int(pred[i][j, 3])), (0, 0, 255), 2)
        for j in range(truth[i].shape[0]):
            cv2.rectangle(col_img, (int(truth[i][j, 0]), int(truth[i][j, 1])),  (int(truth[i][j, 2]), int(truth[i][j, 3])), (0, 255, 0), 1)

        cv2.imwrite(f"./res-img-{i}.png", col_img)

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    print("Loading")
    truth, img =  load_xml(namespace.path) if namespace.type == 'xml' else load_csv(namespace.path)
    print(f"Loaded {len(img)} images")
    print("Calculating")
    pred = evaluateLOGbatch(img)
    meanAp, f1 = meanAveragePrecision(pred, truth)
    print(f"meanAP: {meanAp}, mean f1: {f1}")
    if namespace.draw:
        print("Drawing")
        draw(img, truth, pred)
    print("Finished")
