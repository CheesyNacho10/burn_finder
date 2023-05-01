import cv2
import time
from ultralytics import YOLO
import numpy as np

our_labels = ['1st degree', '2nd degree', '3rd degree']

def AnalyzeCam(device_index, capture_fps, update_ui, stop_thread):
    cap = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
    # Iniciar timer
    start_time = time.time()

    while not stop_thread.is_set():
        # Leer fotograma
        ret, frame = cap.read()

        # Descartar fotogramas si es necesario
        if capture_fps != -1 and time.time() - start_time < 1.0 / capture_fps:
            continue
        else: # Reiniciar timer
            start_time = time.time()

        # Comprobar si se ha leído correctamente el fotograma
        if not ret:
            break

        frame = AnalyzeFrame(frame)

        update_ui(frame)

    # Liberar capturadora y cerrar ventanas
    cap.release()

def AnalyzeVideo(video_path, capture_fps, update_ui, stop_thread):
    cap = cv2.VideoCapture(video_path)
    file_fps = cap.get(cv2.CAP_PROP_FPS)
    fps_ratio = file_fps / capture_fps
    if (fps_ratio < 1):
        fps_ratio = 1
    frame_count = fps_ratio

    while not stop_thread.is_set():
        cap.grab()

        # Descartar fotogramas si es necesario
        frame_count += 1
        if frame_count < fps_ratio:
            continue
        else: # Reiniciar contador
            frame_count = 0

        # Leer el siguiente fotograma del archivo de vídeo
        ret, frame = cap.retrieve()

        # Comprobar si se ha leído correctamente el fotograma
        if not ret:
            break

        frame = AnalyzeFrame(frame)

        # Mostrar fotograma
        update_ui(frame)

    # Liberar capturadora y cerrar ventanas
    cap.release()

def AnalyzeImage(image_path, update_ui):
    frame = cv2.imread(image_path)
    frame = AnalyzeFrame(frame)
    update_ui(frame)

def AnalyzeFrame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    model = YOLO(model="./resources/model_large.pt")
    results = model(frame)

    for result in results:
        for box in result.boxes:
            x, y, w, h = box.xywh.numpy().astype(int)[0]
            pt1 = (int(x - w / 2), int(y - h / 2))
            pt2 = (int(x + w / 2), int(y + h / 2))
            tpt = pt1[0] + 5, pt1[1] + 25
            cv2.rectangle(frame, pt1, pt2, (0, 255, 0), thickness=2)
            cv2.putText(frame, model.names[int(box.cls.item())].capitalize()\
                        + " " + str(round(box.conf.item(), 2)), tpt, cv2.FONT_HERSHEY_SIMPLEX,\
                        0.9, (255, 255, 0), thickness=2)
    
    return frame
