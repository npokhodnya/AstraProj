from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool, QSize
from typing import Callable
import cv2
from ai import ai


class CameraUi(QPushButton):
    def __init__(self, button_id: int, function_for_click: Callable, vertical_layout):
        super().__init__()
        self.camera_id = button_id
        self.setText(f"camera {button_id}")
        self.setObjectName(f"camera{button_id}")
        self.setStyleSheet("QPushButton{\n"
                           "    border: none;\n"
                           "    background-color: none;\n"
                           "}\n"
                           "QPushButton:hover{\n"
                           "    color: rgb(255, 255, 255);\n"
                           "}")
        vertical_layout.addWidget(self)
        self.clicked.connect(lambda: function_for_click(self.camera_id))

    def set_name(self, new_name: str):
        self.setText(new_name)
        self.setObjectName(new_name)


class CameraOutputProcess(QRunnable):
    def __init__(self, video_widget: QLabel, camera_or_file: str | int):
        super(CameraOutputProcess, self).__init__()
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
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                self.video_widget.setPixmap(QPixmap.fromImage(image))
                frame_speed += 1

    def resize_video(self):
        self.video_size = QSize(self.video_widget.size().width(), self.video_widget.size().height())


class Cameras:
    def __init__(self):
        self.buttons: list[CameraUi] = []
        self.processes: list[CameraOutputProcess] = []
        self.open_camera_id = 0
        self.threadpool = QThreadPool()

    def add_cameras(self, main_video: QLabel, cameras_layout: QVBoxLayout):
        cameras_list = Cameras.find_cameras()
        for i in cameras_list:
            new_camera = CameraUi(i, self.change_main_camera, cameras_layout)
            new_process = CameraOutputProcess(main_video, i)
            self.buttons.append(new_camera)
            self.processes.append(new_process)
            self.threadpool.start(self.processes[i])

    def change_main_camera(self, camera_id: int):
        self.processes[self.open_camera_id].is_running = False
        self.processes[camera_id].is_running = True
        self.open_camera_id = camera_id

    @staticmethod
    def find_cameras():
        cameras = []
        camera_number = 0
        while cv2.VideoCapture(camera_number).isOpened():
            cameras.append(camera_number)
            camera_number += 1
        return cameras

    def start_displaying(self):
        self.processes[0].is_running = True
        self.resize_all_videos()

    def stop_displaying(self):
        self.processes[0].is_running = False

    def stop_all_processes(self):
        for process in self.processes:
            process.process_is_worked = False

    def resize_all_videos(self):
        for process in self.processes:
            process.resize_video()
