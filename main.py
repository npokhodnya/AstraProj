import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSlot

from app import Ui_MainWindow

import cv2


class Camera(QPushButton):
    def __init__(self, button_id, function_for_click, parent, vertical_layout):
        super().__init__(parent=parent)
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

    def set_name(self, new_name):
        self.setText(new_name)
        self.setObjectName(new_name)


class CameraOutputProcess(QRunnable):
    def __init__(self, video_widget: Camera, camera_or_file):
        super(CameraOutputProcess, self).__init__()
        self.camera_or_file = camera_or_file
        self.video_widget = video_widget
        self.is_running = False

    @pyqtSlot()
    def run(self):
        self.showing_video()

    def showing_video(self):
        video_size = self.video_widget.size()
        video = cv2.VideoCapture(self.camera_or_file)

        frame_speed = 0

        while True:
            if self.is_running:
                ret, image = video.read()
                image = cv2.resize(image, (video_size.width(), video_size.height()))
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
                self.video_widget.setPixmap(QPixmap.fromImage(image))
                frame_speed += 1


class AttentionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_path = 0
        self.buttons = []
        self.processes = []
        self.open_camera_id = 0
        self.threadpool = QThreadPool()
        self.add_cameras()
        self.processes[0].is_running = True

    def add_cameras(self):
        cameras_list = AttentionApp.find_cameras()
        for i in cameras_list:
            new_camera = Camera(i, self.change_main_camera, self.ui.layoutWidget, self.ui.cameras)
            new_process = CameraOutputProcess(self.ui.MainVideo, i)
            self.buttons.append(new_camera)
            self.processes.append(new_process)
            self.threadpool.start(self.processes[i])

    def change_main_camera(self, camera_id):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttentionApp()
    window.show()
    sys.exit(app.exec())
