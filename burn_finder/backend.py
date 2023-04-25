import cv2
import time
from ultralytics import YOLO
import numpy as np

our_labels = ['1st degree', '2nd degree', '3rd degree']

def AnalyzeCam(device_index, capture_fps, update_ui):
    cap = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
    return AnalyzeCap(cap, capture_fps, update_ui)

def AnalyzeVideo(video_path, capture_fps, update_ui):
    cap = cv2.VideoCapture(video_path)
    return AnalyzeCap(cap, capture_fps, update_ui)

def AnalyzeCap(cap, capture_fps, update_ui):
    # Iniciar timer
    start_time = time.time()

    still_analyzing = True

    while still_analyzing:
        # Leer fotograma
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Descartar fotogramas si es necesario
        if capture_fps != -1 and time.time() - start_time < 1.0 / capture_fps:
            continue
        else: # Reiniciar timer
            start_time = time.time()

        # Comprobar si se ha leído correctamente el fotograma
        if not ret:
            break

        frame = AnalyzeFrame(frame)

        # Mostrar fotograma
        still_analyzing = update_ui(frame)

    # Liberar capturadora y cerrar ventanas
    cap.release()

def AnalyzeFrame(frame):
    # Detectar objetos con YOLOv8z
    model = YOLO(model="./resources/model_medium.pt")
    results = model(frame)

    for result in results:
        for box in result.boxes:
            if box.conf > 0.2 and model.names[int(box.cls.item())] in our_labels:
                x, y, w, h = box.xywh.numpy().astype(int)[0]
                pt1 = (int(x - w / 2), int(y - h / 2))
                pt2 = (int(x + w / 2), int(y + h / 2))
                tpt = pt1[0] + 5, pt1[1] + 25
                cv2.rectangle(frame, pt1, pt2, (0, 255, 0), thickness=2)
                cv2.putText(frame, model.names[int(box.cls.item())].capitalize() + " " + str(round(box.conf.item(), 2)), tpt, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), thickness=2)
    
    return frame
