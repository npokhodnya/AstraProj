from PyQt6.QtWidgets import QPushButton
from typing import Callable


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
