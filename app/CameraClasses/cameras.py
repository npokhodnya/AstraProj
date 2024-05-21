from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import QThreadPool
import cv2
from app.CameraClasses.camera_processes import AiHandler, CameraOutputProcess
from app.CameraClasses.camera_ui import CameraUi


class Cameras:
    def __init__(self):
        self.buttons: list[CameraUi] = []
        self.camera_processes: list[CameraOutputProcess] = []
        self.ai_processes: list[AiHandler] = []
        self.open_camera_id = 0
        self.threadpool = QThreadPool()

    def add_cameras(self, main_video: QLabel, cameras_layout: QVBoxLayout):
        cameras_list = Cameras.find_cameras()
        print(cameras_list)
        cameras_list.pop(1)
        print(cameras_list)
        for i in range(len(cameras_list)):
            new_camera = CameraUi(i, self.change_main_camera, cameras_layout)
            self.buttons.append(new_camera)
            new_ai_process = AiHandler(1)
            new_ai_process.to_behind_window()
            self.ai_processes.append(new_ai_process)
            self.threadpool.start(self.ai_processes[i])
            new_camera_process = CameraOutputProcess(main_video, i, self.ai_processes[i])
            self.camera_processes.append(new_camera_process)
            self.threadpool.start(self.camera_processes[i])
 
    def change_main_camera(self, camera_id: int):
        self.camera_processes[self.open_camera_id].is_running = False
        self.ai_processes[self.open_camera_id].to_behind_window()
        self.camera_processes[camera_id].is_running = True
        self.ai_processes[camera_id].to_main_window()
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
        self.camera_processes[0].is_running = True
        self.ai_processes[0].to_main_window()
        self.resize_all_videos()

    def stop_all_cameras(self):
        for i in range(len(self.camera_processes)):
            self.camera_processes[i].process_is_worked = False
            self.ai_processes[i].stop_checking()

    def resize_all_videos(self):
        for process in self.camera_processes:
            process.resize_video()
