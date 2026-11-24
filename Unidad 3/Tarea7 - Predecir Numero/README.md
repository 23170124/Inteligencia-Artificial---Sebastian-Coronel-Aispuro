# Tarea 7 – Predecir número (MNIST)

**Alumno:** Sebastian Coronel Aispuro

Red neuronal multicapa (MLP) de scikit-learn entrenada con las 70,000 imágenes de dígitos escritos a mano de MNIST (60,000 para entrenar y 10,000 para probar).

- Capas ocultas: 128 y 64 neuronas, activación ReLU, optimizador Adam
- Se detiene sola cuando la validación deja de mejorar (early stopping)
- `resultados.png`: curva de entrenamiento, matriz de confusión y ejemplos mal clasificados
- `app.py`: ventana para dibujar un número con el mouse; muestra la predicción y la probabilidad de cada dígito

