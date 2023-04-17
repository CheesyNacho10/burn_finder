from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO('yolov8s.pt')  # load an official modeled

    model.train(data='C:/Users/Nacho/Desktop/yolo_anal/version_benchmark/v8/datasets/Hudyakova-1/data.yaml', imgsz=320, device=0, workers=1)

    # Export the model
    model.export()