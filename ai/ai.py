from ultralytics import YOLO
import torch
import numpy

model_path = "C:/Users/lexte/Desktop/AstraProject/ai/best.pt"
model_version = "v5"
model = YOLO(model_path, model_version)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(device)


def predict(frame) -> list:
    frame = numpy.asarray(frame)
    result = model.predict(source=frame)
    return [result, model.names]
