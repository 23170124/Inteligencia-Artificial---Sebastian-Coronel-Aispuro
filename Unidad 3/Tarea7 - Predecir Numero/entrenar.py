from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from sklearn.neural_network import MLPClassifier

CARPETA = Path(__file__).parent

print("Descargando MNIST (solo la primera vez)...")
X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
X = X.astype(np.float32) / 255.0
y = y.astype(int)

X_ent, X_pru = X[:60000], X[60000:]
y_ent, y_pru = y[:60000], y[60000:]

red = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    activation="relu",
    solver="adam",
    batch_size=256,
    max_iter=25,
    early_stopping=True,
    n_iter_no_change=4,
    random_state=0,
    verbose=True,
)
red.fit(X_ent, y_ent)

pred = red.predict(X_pru)
print(f"\nExactitud en prueba: {accuracy_score(y_pru, pred) * 100:.2f}%")

joblib.dump(red, CARPETA / "modelo_mnist.joblib")
print("Modelo guardado en modelo_mnist.joblib")

fig, ax = plt.subplots(1, 3, figsize=(17, 5))

ax[0].plot(red.loss_curve_, label="perdida")
ax[0].plot(red.validation_scores_, label="exactitud validacion")
ax[0].set_xlabel("epoca")
ax[0].set_title("Entrenamiento")
ax[0].legend()

ConfusionMatrixDisplay.from_predictions(y_pru, pred, ax=ax[1], colorbar=False)
ax[1].set_title("Matriz de confusion")
ax[1].set_xlabel("predicho")
ax[1].set_ylabel("real")

ax[2].axis("off")
errores = np.flatnonzero(pred != y_pru)[:8]
for i, k in enumerate(errores):
    sub = fig.add_subplot(2, 12, 9 + (i % 4) + (i // 4) * 12)
    sub.imshow(X_pru[k].reshape(28, 28), cmap="gray")
    sub.set_title(f"r:{y_pru[k]} p:{pred[k]}", fontsize=8)
    sub.axis("off")
ax[2].set_title("Algunos errores (r=real, p=predicho)")

plt.tight_layout()
plt.savefig(CARPETA / "resultados.png", dpi=120)
plt.show()
