"""
Materia: Inteligencia Artificial
Profesor: Jose Mario Rios Felix
Integrantes:
- Angulo Aviles Atanacio Alejandro
- Jouse Alfonso Beltran Meza
- Sebastian Coronel Aispuro
- Franciso Alonzo Lopez Murguia
"""
import json
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


DATA_DIR = "dataset"
IMG = 128               # tamaño uniforme 128 x 128
BATCH = 32
EPOCHS_FASE1 = 30       # cabeza nueva (EarlyStopping lo corta antes si ya no mejora)
EPOCHS_FASE2 = 20       # fine-tuning
CAPAS_A_AJUSTAR = 30    # cuántas capas finales de MobileNetV2 se descongelan
SEED = 42

#  1. Dataset 
# 80 entrenamiento y 20 validación (sin test, como pide la práctica).
# label_mode="categorical" -> etiquetas one-hot, necesarias para
# categorical_crossentropy.
train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR, validation_split=0.2, subset="training", seed=SEED,
    image_size=(IMG, IMG), batch_size=BATCH, label_mode="categorical")
val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR, validation_split=0.2, subset="validation", seed=SEED,
    image_size=(IMG, IMG), batch_size=BATCH, label_mode="categorical")

clases = train_ds.class_names
NUM_CLASES = len(clases)
print("Clases:", clases)
with open("clases.json", "w", encoding="utf-8") as f:
    json.dump(clases, f, ensure_ascii=False)

# prefetch: prepara el siguiente lote mientras se entrena con el actual
train_ds = train_ds.shuffle(1000).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

#  2. Data Augmentation 
augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),   # volteo horizontal
    layers.RandomRotation(0.08),       # rotación
    layers.RandomZoom(0.15),           # zoom
    layers.RandomBrightness(0.2),      # cambios de iluminación
    layers.RandomContrast(0.2),
], name="augmentation")

#  3. Modelo 
# Base: MobileNetV2 con pesos de ImageNet, SIN su capa de clasificación final
# (include_top=False). Contiene todas las capas convolucionales.
base = keras.applications.MobileNetV2(
    input_shape=(IMG, IMG, 3), include_top=False, weights="imagenet")
base.trainable = False  # Fase 1: congelada


entrada = keras.Input(shape=(IMG, IMG, 3)) 
x = augmentation(entrada)
x = layers.Rescaling(1.0 / 127.5, offset=-1)(x)  # normaliza a [-1, 1] lo que espera MobileNetV2
x = base(x, training=False)                      # training=False: mantiene BatchNorm de la base estable
x = layers.GlobalAveragePooling2D()(x)           # agrupamiento: promedia cada mapa de características
x = layers.BatchNormalization()(x)               # regularización
x = layers.Dropout(0.4)(x)                       # regularización
x = layers.Dense(128, activation="relu")(x)      # cabeza nueva
x = layers.Dropout(0.4)(x)
salida = layers.Dense(NUM_CLASES, activation="softmax")(x)  # 1 neurona por persona

model = keras.Model(entrada, salida, name="mobilenetv2_rostros")
model.summary()

#  4. Callbacks 
callbacks = [
    # Guarda el mejor modelo
    keras.callbacks.ModelCheckpoint("mejor_modelo.keras", monitor="val_loss",
                                    save_best_only=True, verbose=1),
    # Si val_loss no mejora en 6 épocas, para y regresa a los mejores pesos
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=6,
                                  restore_best_weights=True),
    # Si se estanca, baja el learning rate a la mitad
    keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3),
]

#  5. Fase 1: entrenar el modelo de 1d 
model.compile(optimizer=keras.optimizers.Adam(1e-3),
              loss="categorical_crossentropy",   # clasificación multiclase
              metrics=["accuracy"])
print("\n=== FASE 1: entrenando la cabeza nueva (base congelada) ===")
hist1 = model.fit(train_ds, validation_data=val_ds,
                  epochs=EPOCHS_FASE1, callbacks=callbacks)

#  6. Fase 2: entrenamiento mas fino 
base.trainable = True
for capa in base.layers[:-CAPAS_A_AJUSTAR]:
    capa.trainable = False   # solo se ajustan las últimas capas

# Hay que volver a compilar después de cambiar trainable.
# Learning rate MUY bajo para no destruir lo que MobileNetV2 ya sabe.
model.compile(optimizer=keras.optimizers.Adam(1e-5),
              loss="categorical_crossentropy",
              metrics=["accuracy"])
print("\n=== FASE 2: fine-tuning de las últimas capas ===")
hist2 = model.fit(train_ds, validation_data=val_ds,
                  epochs=EPOCHS_FASE2, callbacks=callbacks)

# 7. Curvas
def unir(clave):
    return hist1.history[clave] + hist2.history[clave]


fase2_inicio = len(hist1.history["loss"])
plt.figure(figsize=(12, 4))
for i, (clave, titulo) in enumerate([("loss", "Pérdida (loss)"),
                                     ("accuracy", "Precisión (accuracy)")], 1):
    plt.subplot(1, 2, i)
    plt.plot(unir(clave), label="entrenamiento")
    plt.plot(unir("val_" + clave), label="validación")
    plt.axvline(fase2_inicio - 1, color="gray", linestyle="--", label="inicio fine-tuning")
    plt.title(titulo)
    plt.xlabel("época")
    plt.legend()
plt.tight_layout()
plt.savefig("curvas.png", dpi=150)
plt.show()

#  8. Resultado final 
mejor = keras.models.load_model("mejor_modelo.keras")
loss, acc = mejor.evaluate(val_ds, verbose=0)
print(f"\nMejor modelo -> val_loss: {loss:.4f} | val_accuracy: {acc:.4f}")