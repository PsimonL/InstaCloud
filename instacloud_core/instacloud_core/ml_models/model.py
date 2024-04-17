# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO
import os


def predict_class(path_to_photo):
    """
    Predict the class
    :param path_to_photo: path to the image to predict
    :return: the class of the image
    """
    model = YOLO(r'../ml_models/InstaCloud.pt')
    source = cv2.imread(path_to_photo)
    results = model.predict(source, verbose=False)
    return results[0].names[results[0].boxes.cls[0].item()]


if __name__ == '__main__':
    print(predict_class('tests/kot.jpg'))
