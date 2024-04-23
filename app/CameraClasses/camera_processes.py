import time
import requests
from numpy import ndarray
from ultralytics.utils.plotting import Annotator
from PyQt6.QtCore import QRunnable, pyqtSlot, QSize
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel
import cv2
import json_checker
import json
from ai import ai


class AiHandler(QRunnable):
    def __init__(self, ai_check_frequency: float):
        super(AiHandler, self).__init__()
        self.ai_result = []
        self.server_date = json_checker.get_data()
        self.ai_check_frequency = ai_check_frequency
        self.last_time = time.time()
        self.tasks = []
        self.is_checking = True
        self.url = f"http://{self.server_date["server_ip"]}:{self.server_date["server_port"]}/"

    def turn_it_image(self, image: ndarray) -> ndarray:
        if not self.ai_result:
            return image

        annotator = Annotator(image)
        categories = self.ai_result[1]
        ai_data = self.ai_result[0]

        for i in ai_data:
            boxes = i.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                annotator.box_label(b, categories[int(c)])

        image = annotator.result()
        return image

    def to_main_window(self):
        self.ai_check_frequency /= 2

    def to_behind_window(self):
        self.ai_check_frequency *= 2

    def add_image_to_task_list(self, image: list):
        self.tasks.append(image)

    def stop_checking(self):
        self.is_checking = False

    @pyqtSlot()
    def run(self):
        self.start_check_loop()

    def start_check_loop(self):
        while self.is_checking:
            print(len(self.tasks))
            if len(self.tasks) > 0:
                task_id = len(self.tasks) - 1
                self.check_image(self.tasks[task_id])
                self.tasks.pop(task_id)

    def check_image(self, image: ndarray):
        print("checked")
        self.ai_result = ai.predict(image)


class CameraOutputProcess(QRunnable):
    def __init__(self, video_widget: QLabel, camera_or_file: str | int, ai_handler: AiHandler):
        super(CameraOutputProcess, self).__init__()
        self.ai_handler = ai_handler
        self.camera_or_file = camera_or_file
        self.video_widget = video_widget
        self.is_running = False
        self.process_is_worked = True
        self.video_size = video_widget.size()

    @pyqtSlot()
    def run(self):
        self.showing_video()

    def showing_video(self):
        self.resize_video()
        video = cv2.VideoCapture(self.camera_or_file)
        frame_speed = 0
        while self.process_is_worked:
            if self.is_running:
                ret, image = video.read()
                image = cv2.resize(image, (self.video_size.width(), self.video_size.height()))
                self.ai_handler.add_image_to_task_list(image)
                image = self.ai_handler.turn_it_image(image)
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                self.video_widget.setPixmap(QPixmap.fromImage(image))
                frame_speed += 1

    def resize_video(self):
        self.video_size = QSize(self.video_widget.size().width(), self.video_widget.size().height())
