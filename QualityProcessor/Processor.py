import numpy as np


def meanAveragePrecision(pred:list, truth:list):
    results = np.empty((len(truth), 3))
    for b in range(len(truth)):
        truePositive = iouBatch(pred[b], truth[b])
        truthCount = truth[b].shape[0]
        truePositiveCumulative = np.cumsum(truePositive)
        falsePositiveCumulative = np.cumsum(1 - truePositive)
        recallCurve = truePositiveCumulative / (truthCount + 1e-16)
        precisionCurve = truePositiveCumulative / (truePositiveCumulative + falsePositiveCumulative)
        ap = averagePrecision(recallCurve, precisionCurve)
        results[b] = np.array([recallCurve[-1], precisionCurve[-1], ap])
    precision = results[:, 1]
    recall = results[:, 0]
    ap = results[:, 2]
    f1 = 2 * precision * recall / (precision + recall + 1e-16)
    return np.nanmean(ap), np.nanmean(f1)

def averagePrecision(recall, precision):
    # correct AP calculation
    # first append sentinel values at the end
    mrec = np.concatenate(([0.0], recall, [1.0]))
    mpre = np.concatenate(([0.0], precision, [0.0]))

    # compute the precision envelope
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

    # to calculate area under PR curve, look for points
    # where X axis (recall) changes value
    i = np.where(mrec[1:] != mrec[:-1])[0]

    # and sum (\Delta recall) * prec
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def iouBatch(pred:np.ndarray, truth:np.ndarray):
    truePositives = np.zeros(pred.shape[0])
    truth_checked = []
    for i in range(pred.shape[0]):
        iouRes = iouRow(pred[i], truth)
        maxIouInd = np.argmax(iouRes)
        if maxIouInd not in truth_checked and iouRes[maxIouInd] > 0.5:
            truePositives[i] = 1
            truth_checked.append(maxIouInd)
    return truePositives

def iouRow(pred:np.ndarray, truth:np.ndarray):
    xA = np.maximum(pred[0], truth[:, 0])
    yA = np.maximum(pred[1], truth[:, 1])
    xB = np.minimum(pred[2], truth[:, 2])
    yB = np.minimum(pred[3], truth[:, 3])

    interArea = np.abs(np.maximum(xB - xA, 0) * np.maximum(yB - yA, 0))

    predArea = np.abs((pred[2] - pred[0]) * (pred[3] - pred[1]))
    truthArea = np.abs((truth[:, 2] - truth[:, 0]) * (truth[:, 3] - truth[:, 1]))
    unionArea = (truthArea + predArea - interArea)
    iou = np.true_divide(interArea, unionArea,
                    out=np.zeros_like(unionArea),
                    where=np.logical_and(interArea > 0, unionArea > 0))
    return iou