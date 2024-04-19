from ultralytics import YOLO

model_path = "C:/Users/lexte/Desktop/AstraProject/ai/best.pt"
model_version = "v5"
model = YOLO(model_path, model_version)


def predict(frame):
    detected_boxes = model.predict(source=frame)
    return detected_boxes[0]
