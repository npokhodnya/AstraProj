from PyQt6.QtWidgets import QApplication, QMainWindow
from app.ui.app import Ui_MainWindow
from app.CameraClasses.cameras import Cameras
import sys
import requests
import json_checker


class AttentionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = json_checker.get_data()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_path = 0
        self.resize(self.ui.frame.size())
        self.cameras = Cameras()
        print("added")
        self.cameras.add_cameras(self.ui.main_video, self.ui.cameras)
        self.cameras.start_displaying()

    def closeEvent(self, event):
        requests.post(f"http://{self.data["server_ip"]}:{self.data["server_port"]}/stop_server")
        self.cameras.stop_all_processes()
        event.accept()

    def resizeEvent(self, event):
        self.cameras.resize_all_videos()
        event.accept()


def start():
    app = QApplication(sys.argv)
    window = AttentionApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start()
