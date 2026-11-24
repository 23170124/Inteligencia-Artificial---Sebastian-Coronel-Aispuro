"""
Materia: Inteligencia Artificial
Profesor: Jose Mario Rios Felix
Integrantes:
- Angulo Aviles Atanacio Alejandro
- Jouse Alfonso Beltran Meza
- Sebastian Coronel Aispuro
- Franciso Alonzo Lopez Murguia
"""

import cv2
import os
import time

CARPETA_SALIDA ="dataset_Nombre" 
FOTOS_POR_POSE = 20  

POSES = [
    "1/5: Mira DE FRENTE (expresion normal)",
    "2/5: Gira un poco a la IZQUIERDA",
    "3/5: Gira un poco a la DERECHA",
    "4/5: Inclina un poco ARRIBA",
    "5/5: Inclina un poco ABAJO / sonrie"
]

os.makedirs(CARPETA_SALIDA, exist_ok=True)

# Cargar el detector de  OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
contador_total = 0


for instruccion in POSES:
# 1. Preparacion para tomar fotos
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < 3.5:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)  
        
        restante = int(3.5 - (time.time() - tiempo_inicio)) + 1
        cv2.putText(frame, instruccion, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
        cv2.putText(frame, f"Preparate... {restante}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
        
        cv2.imshow("Generador de Dataset Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

# 2. captura de fotografias 
    fotos_pose = 0
    while fotos_pose < FOTOS_POR_POSE:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detecta rostros
        rostros = face_cascade.detectMultiScale(gris, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in rostros:
            # Recortar la cara y redimensionar a un tamaño estandar
            rostro_recortado = frame[y:y+h, x:x+w]
            rostro_redim = cv2.resize(rostro_recortado, (200, 200))
            
            # Guardar imagen
            contador_total += 1
            fotos_pose += 1
            ruta = os.path.join(CARPETA_SALIDA, f"cara_{contador_total:03d}.jpg")
            cv2.imwrite(ruta, rostro_redim)

            # Dibujar cuadro verde para confirmar que sí está capturando
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Pausa para registrar bien las fotos
            cv2.waitKey(100)
            break  # Solo guarda una cara por frame

        # Mostrar progreso en pantalla
        cv2.putText(frame, instruccion, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.putText(frame, f"Capturando: {contador_total}/100", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.imshow("Generador de Dataset Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

print(f"Se guardaron {contador_total} imagenes en la carpeta '{CARPETA_SALIDA}'.")
cap.release()
cv2.destroyAllWindows()