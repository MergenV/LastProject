import cv2
import numpy as np


class Cnn:
    net: cv2.dnn_Net
    confidence_idx: float
    threshold_idx: float

    def __init__(self, weights_path: str, config_path: str, confidence_idx, threshold_idx):
        """

        :param weights_path: Путь к файлу весов
        :param config_path: Путь к файлу конфигов
        :param confidence_idx: %ный порог уверенности для детекшна
        :param threshold_idx: порог для удаления накладывающихся детекшнов
        """

        # Создаем объект net из OpenCv для инференса
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        self.confidence_idx = confidence_idx
        self.threshold_idx = threshold_idx
        ln = self.net.getLayerNames()
        self.ln = [ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def get_bboxes(self, image) -> (list[list[float]], list[float]):
        """

        :param image: Картинка для распознавания
        :return: координаты боксов списком, уровени уверенности списком, id классов списком
        """

        # создаем blob из входной картинки
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (256, 256), swapRB=True, crop=False)

        # Пускаем blob на вход и прогоняем по слоям нейросети
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.ln)

        # Задаем пустые списки для последующего заполнения данными
        boxes = []
        initial_boxes = []
        final_boxes = []

        confidences = []
        final_confidences = []

        class_ids = []
        final_class_ids = []

        # Итерируем по всем результатам
        for output in layer_outputs:
            for detection in output:
                # Отделяем информацию о id классов
                scores = detection[5:]
                # Ищем максимальный процент совпадения среди всех классов и запоминаем класс
                class_id = np.argmax(scores)
                # Записываем максимальный процент совпадения
                confidence = scores[class_id]
                # Если процент уверенности больше заданного порога
                if confidence > self.confidence_idx:
                    # Cчитываем координаты и находим координаты углов для создания прямоугольника
                    box = np.around(detection[0:4], 2)
                    initial_boxes.append(box)
                    (centerX, centerY, width, height) = box
                    x = centerX - (width / 2)
                    y = centerY - (height / 2)
                    # Заполняем соответствующие списки этими данными
                    boxes.append([x, y, width, height])
                    confidences.append(confidence)
                    class_ids.append(class_id)
        # Функция для удаления накладывающихся детекшнов по площади их пересечения
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_idx, self.threshold_idx)

        # Оставшиеся детекшны добавляем в финальный результат
        if len(idxs) > 0:
            for i in idxs:
                final_boxes.append(initial_boxes[i])
                final_confidences.append(confidences[i])
                final_class_ids.append(class_ids[i])
            return final_boxes, final_confidences, final_class_ids
        else:
            return None, None, None

    def draw_boxes(self, boxes, image, color=(0, 255, 0), thickness=1, confidences=None, classes=None, labels=None):
        """

        :param boxes: боксы(кординаты прямоугольников для отрисовки)
        :param image: Картинка для отрисовки
        :param color: цвет
        :param thickness: толщина шрифта и прямоугольника
        :param confidences: список из соответствующих % уверренности (для вывода в виде надписи над прямоугльником)
        :param classes: список из соответствующих id классов (для вывода в виде надписи над прямоугльником)
        :param labels: список из соответствующих названий классов (для вывода в виде надписи над прямоугльником)
        :return: картинка с отрисованными результатами распознавания
        """
        (H, W) = image.shape[:2]
        copy = image.copy()
        # Если результатов распознавания нет возвращаем ту же картинку
        if boxes is None:
            return copy
        # Если помимо координат прямоугльников даны необязательные параметры confidences, classes, labels
        if confidences is not None:
            # Округляем до двух знаков после запятой
            confidences = np.around(confidences, 2)
            # Для каждого элемента
            for bb, conf, class_id in zip(boxes, confidences, classes):
                # Вычисляем координаты
                (centerX, centerY, width, height) = bb * np.array([W, H, W, H])
                x1 = int(centerX - (width / 2))
                y1 = int(centerY - (height / 2))
                x2 = int(centerX + (width / 2))
                y2 = int(centerY + (height / 2))
                # Рисуем прямоугольник
                cv2.rectangle(copy, (x1, y1), (x2, y2), color, thickness)
                # Накладываем текст
                cv2.putText(copy, '{}: {:.2f}'.format(labels[class_id], conf), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                            thickness)
                # По центру рисуем точку
                cv2.circle(copy, (int(centerX), int(centerY)), 1, color, -1)
        # То же самое но рисуем только прямоугольники
        else:
            for bb in boxes:
                (centerX, centerY, width, height) = bb * np.array([W, H, W, H])
                x1 = int(centerX - (width / 2))
                y1 = int(centerY - (height / 2))
                x2 = int(centerX + (width / 2))
                y2 = int(centerY + (height / 2))
                cv2.rectangle(copy, (x1, y1), (x2, y2), color, thickness)
        return copy
