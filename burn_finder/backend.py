import cv2
import time

# POR REVISAR

def capture_video(device_index, capture_fps):
    cap = cv2.VideoCapture(device_index)
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, capture_fps)

    # Iniciar timer
    start_time = time.time()

    while True:
        # Leer fotograma
        ret, frame = cap.read()

        # Descartar fotogramas si es necesario
        if capture_fps != -1 and time.time() - start_time < 1.0 / capture_fps:
            continue

        # Reiniciar timer
        start_time = time.time()

        # Comprobar si se ha leído correctamente el fotograma
        if not ret:
            break

        # Detectar objetos con YOLOv8
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Dibujar boxes en el fotograma
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    w = int(detection[2] * frame.shape[1])
                    h = int(detection[3] * frame.shape[0])
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Mostrar fotograma
        cv2.imshow("Video", frame)

        # Esperar a pulsar una tecla para salir
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Liberar capturadora y cerrar ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_video(0, 30)