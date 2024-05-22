from app.violation_detector.violation_classes import Violation, Vest, Helmet
from ultralytics.engine.results import Boxes


class Detector:
    def __init__(self):
        self.classes: list[Violation] = [Vest(), Helmet()]

    def check_violations(self, boxes: Boxes) -> Violation | None:
        for violation_class in self.classes:
            violation_class.set_boxes(boxes)
            if violation_class.is_warning():
                return violation_class

        return
