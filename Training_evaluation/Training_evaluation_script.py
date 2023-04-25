from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO('yolov8l.pt')  # load an official modeled

    model.train(data='./skin_burn_detection.v7-skin_burn_6.25_19-15.yolov8/data.yaml', imgsz=320, device=0, workers=2, epochs=25)

    # Export the model
    model.export()