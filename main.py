import sys
import time

from pygrabber.dshow_graph import FilterGraph

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot, QEvent

from app import Ui_MainWindow

import cv2


class Camera(QPushButton):
    def __init__(self, button_id, main_app, parent, vertical_layout: QVBoxLayout):
        super().__init__(parent=parent)
        self.app = main_app
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
        self.clicked.connect(self.change_camera)

    def change_camera(self):
        self.app.worker.is_running = False

        self.app.worker = Worker(self.app.ui.MainVideo, self.camera_id)
        self.app.threadpool.start(self.app.worker)


class Worker(QRunnable):
    def __init__(self, video_widget, camera_or_file):
        super(Worker, self).__init__()
        self.camera_or_file = camera_or_file
        self.video_widget = video_widget
        self.is_running = True

    @pyqtSlot()
    def run(self):
        self.showing_video()

    def showing_video(self):
        video_size = self.video_widget.size()
        video = cv2.VideoCapture(self.camera_or_file)
        while self.is_running:
            ret, image = video.read()
            image = cv2.resize(image, (video_size.width(), video_size.height()))
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
            self.video_widget.setPixmap(QPixmap.fromImage(image))


class AttentionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_path = 0
        self.buttons = []
        self.threadpool = QThreadPool()
        self.worker = Worker(self.ui.MainVideo, self.file_path)
        self.worker.autoDelete()
        self.threadpool.start(self.worker)
        self.add_cameras()

    def add_cameras(self):
        cameras_list = AttentionApp.find_cameras()
        margin = 0
        for i in cameras_list:
            new_camera = Camera(i, self, self.ui.layoutWidget, self.ui.cameras)
            self.buttons.append(new_camera)
            print(self.buttons)
            margin += 30

    @staticmethod
    def find_cameras():
        cameras = []
        camera_number = 0

        while cv2.VideoCapture(camera_number).isOpened():
            cameras.append(camera_number)
            camera_number += 1
        print(cameras)
        return cameras


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttentionApp()
    window.show()
    sys.exit(app.exec())
