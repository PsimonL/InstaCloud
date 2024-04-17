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
    # Get the directory of the current script
    current_dir = os.path.dirname(__file__)
    # Construct the model path relative to the current script
    model_path = os.path.join(current_dir, '..', 'ml_models', 'InstaCloud.pt')
    model = YOLO(model_path)
    source = cv2.imread(path_to_photo)
    results = model.predict(source, verbose=False)
    return results[0].names[results[0].boxes.cls[0].item()]


if __name__ == '__main__':
    print(predict_class('tests/kot.jpg'))
