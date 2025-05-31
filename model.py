from ultralytics import YOLO



# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

results = model(source=2, show=True, conf=0.2, device= 0, stream=False)
