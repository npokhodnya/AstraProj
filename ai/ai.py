from ultralytics import YOLO
import torch
import numpy

model_path = "../ai/best.pt"
model_version = "v8"
model = YOLO(model_path, model_version)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
model.to(device)


def predict(frame) -> list:
    frame = numpy.asarray(frame)
    result = model.predict(source=frame)
    return [result, model.names]
