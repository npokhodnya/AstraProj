from ultralytics.engine.results import Boxes


class Violation:
    def __init__(self):
        self.name_for_app = ""
        self.checked_id: int = -1
        self.main_id: int = -1
        self.box_coefficient: float = 1
        self.all_boxes: Boxes | None = None
        self.main_boxes = []
        self.checked_boxes = []

    def set_boxes(self, boxes: Boxes):
        self.all_boxes = boxes
        for box in boxes:
            if box.cls == self.main_id:
                self.main_boxes.append(box)
            elif box.cls == self.checked_id:
                self.checked_boxes.append(box)

    def check_checked_boxes(self) -> bool:
        for checked in self.checked_boxes:
            if not self.check_main_boxes(checked):
                return False

        return True

    def check_main_boxes(self, checked_box) -> bool:
        for main in self.main_boxes:
            if self.is_warning_for_one_box(checked_box, main):
                return True

        return False

    def is_warning_for_one_box(self, checked_box, main_box) -> bool:
        checked_box = checked_box.xyxy
        main_box = main_box.xyxy
        main_box[3] *= self.box_coefficient
        main_box[1] *= 2 - self.box_coefficient
        comparison_with_top_point = checked_box[0] >= main_box[0] and checked_box[1] <= main_box[1]
        comparison_with_bottom_point = checked_box[2] <= main_box[2] and checked_box[3] >= main_box[3]
        return not comparison_with_top_point and comparison_with_bottom_point


class Vest(Violation):
    def __init__(self):
        super().__init__()
        self.checked_id = 0
        self.name_for_app = "Vest not in human"
        self.main_id = 0
        self.box_coefficient = 1


class Helmet(Violation):
    def __init__(self):
        super().__init__()
        self.checked_id = 0
        self.name_for_app = "Helmet not in human"
        self.main_id = 0
        self.box_coefficient = 1
