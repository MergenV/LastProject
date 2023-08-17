import cv2
from cnn_class import Cnn

cnn = Cnn('yolov4-tiny-obj_3000.weights', 'yolov4-tiny-obj.cfg', 0.5, 0.5)


def get_distance_to_center(image):
    images = cv2.imread(image)
    boxes, confidences, _ = cnn.get_bboxes(images)
    return boxes[0][0] * 256


