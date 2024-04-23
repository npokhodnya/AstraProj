from ultralytics import YOLO
import numpy

model_path = "C:/Users/lexte/Desktop/AstraProject/ai/best.pt"
model_version = "v5"
model = YOLO(model_path, model_version)


def predict(frame: list) -> list:
    frame = numpy.asarray(frame)
    result = model.predict(source=frame)
    return [result, model.names]
