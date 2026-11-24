"""
Materia: Inteligencia Artificial
Profesor: Jose Mario Rios Felix
Integrantes:
- Angulo Aviles Atanacio Alejandro
- Jouse Alfonso Beltran Meza
- Sebastian Coronel Aispuro
- Franciso Alonzo Lopez Murguia
"""

from collections import deque
import json
import cv2
import numpy as np
import tensorflow as tf

IMG = 128          # mismo tamaño que en el entrenamiento
UMBRAL = 0.60      # si la confianza es menor -> "Desconocido"
VENTANA = 8        # n de frames que se promedian (más alto = más estable)
MARGEN = 0.15      # mismo margen que en 1_recortar_rostros.py
CAMARA = 0         # cambia a 1 si usas otra cámara

#  Carga 
model = tf.keras.models.load_model("mejor_modelo.keras")
with open("clases.json", encoding="utf-8") as f:
    clases = json.load(f)

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(CAMARA)
historial = deque(maxlen=VENTANA)  # guarda las últimas predicciones

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)  # efecto espejo

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    caras = detector.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=6,
                                      minSize=(80, 80))

    if len(caras) > 0:
        # Nos quedamos con la cara más grande (la más cercana a la cámara)
        x, y, w, h = max(caras, key=lambda c: c[2] * c[3])
        m = int(MARGEN * w)
        x1, y1 = max(x - m, 0), max(y - m, 0)
        x2, y2 = min(x + w + m, frame.shape[1]), min(y + h + m, frame.shape[0])

        # Preparar el ROI igual que en el entrenamiento (BGR -> RGB, 128x128)
        roi = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
        roi = cv2.resize(roi, (IMG, IMG)).astype("float32")
        # La normalización a [-1,1] ya está DENTRO del modelo (capa Rescaling)

        probs = model(roi[None, ...], training=False).numpy()[0]
        historial.append(probs)

        # Promedio de los ultimos frames predicción estable, sin parpadeos
        prom = np.mean(historial, axis=0)
        idx = int(np.argmax(prom))
        conf = float(prom[idx])

        if conf >= UMBRAL:
            etiqueta, color = f"{clases[idx]} {conf * 100:.1f}%", (0, 200, 0)
        else:
            etiqueta, color = f"Desconocido {conf * 100:.1f}%", (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, etiqueta, (x1 + 3, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    else:
        historial.clear()  # sin cara: reinicia el promedio

    cv2.imshow("Reconocimiento facial - CNN", frame)
    tecla = cv2.waitKey(1) & 0xFF
    if tecla in (27, ord("q")):
        break

cap.release()
cv2.destroyAllWindows()