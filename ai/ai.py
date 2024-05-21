from ultralytics import YOLO
import numpy

model_path = "../ai/best.pt"
model_version = "v5"
model = YOLO(model_path, model_version)


def predict(frame) -> list:
    frame = numpy.asarray(frame)
    result = model.predict(source=frame)
    return [result, model.names]
