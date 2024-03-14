from ultralytics import YOLO
import numpy

model_path = "./model.pt"
model_version = "v8"
model = YOLO(model_path, model_version)


def predict(frame):
    detected_boxes = model.predict(source=frame)
    print("wqdqwdwqdqwdqwd")
    print(detected_boxes[0].numpy())
    return detected_boxes[0].numpy()

