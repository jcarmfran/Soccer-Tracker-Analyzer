from ultralytics import YOLO

model = YOLO("yolov8m")

results = model.predict("artifacts/input_videos/08fd33_4.mp4", save=True)
print(results[0]) # printing first frame
print("=================")
for box in results[0].boxes:
    print(box)