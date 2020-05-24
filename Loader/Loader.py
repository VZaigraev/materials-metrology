import cv2
import pandas as pd
import os
import re
from skimage.filters import gaussian
import numpy as np
from skimage.color import rgb2gray

import xml.etree.ElementTree as ET

def load_xml(dir:str):
    result = ([], [])
    files = os.listdir(dir)
    xmlPat = re.compile("(.*).xml")
    for f in files:
        match = xmlPat.match(f)
        if match:
            name = match.group(1)
            imgPath = os.path.join(dir, name + '.bmp')
            if os.path.exists(imgPath):
                print(f"Loading {name}")
                xml = read_content(os.path.join(dir, f))
                img = cv2.imread(imgPath)[:800]
                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                result[0].append(xml)
                result[1].append(imgGray)
    return result[0], result[1]



def read_content(xml_file: str):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    list_with_all_boxes = []

    for boxes in root.iter('object'):

        filename = root.find('filename').text

        ymin, xmin, ymax, xmax = None, None, None, None

        for box in boxes.findall("bndbox"):
            ymin = int(box.find("ymin").text)
            xmin = int(box.find("xmin").text)
            ymax = int(box.find("ymax").text)
            xmax = int(box.find("xmax").text)

        list_with_single_boxes = [xmin, ymin, xmax, ymax]
        list_with_all_boxes.append(list_with_single_boxes)

    return np.array(list_with_all_boxes)

def load_csv(dir:str):
    result = ([], [])
    files = os.listdir(dir)
    xmlPat = re.compile("(.*).csv")
    for f in files:
        match = xmlPat.match(f)
        if match:
            name = match.group(1)
            imgPath = os.path.join(dir, name + '.png')
            if os.path.exists(imgPath):
                print(f"Loading {name}")
                xml = np.array(pd.read_csv(os.path.join(dir, f)))
                img = cv2.imread(imgPath)[:800]
                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                result[0].append(xml)
                result[1].append(imgGray)
    return result[0], result[1]

