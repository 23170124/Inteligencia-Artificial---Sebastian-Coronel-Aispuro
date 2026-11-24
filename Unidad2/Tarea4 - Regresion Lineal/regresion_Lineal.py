import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing


class RegresionLineal:
    def __init__(self, alpha=0.05, iteraciones=1500):
        self.alpha = alpha
        self.iteraciones = iteraciones
        self.historial = []

    def entrenar(self, X, y):
        m, n = X.shape
        self.w = np.zeros(n)
        self.b = 0.0
        for _ in range(self.iteraciones):
            error = X @ self.w + self.b - y
            self.w -= self.alpha * (X.T @ error) / m
            self.b -= self.alpha * error.mean()
            self.historial.append((error ** 2).mean() / 2)

    def predecir(self, X):
        return X @ self.w + self.b


def r2(y, y_hat):
    return 1 - ((y - y_hat) ** 2).sum() / ((y - y.mean()) ** 2).sum()


datos = fetch_california_housing()
X, y, nombres = datos.data, datos.target, datos.feature_names

rng = np.random.default_rng(7)
idx = rng.permutation(len(X))
corte = int(len(X) * 0.8)
ent, pru = idx[:corte], idx[corte:]

# escalar con la media y desviacion SOLO del entrenamiento
media, desv = X[ent].mean(axis=0), X[ent].std(axis=0)
X_esc = (X - media) / desv

modelo = RegresionLineal()
modelo.entrenar(X_esc[ent], y[ent])
y_pred = modelo.predecir(X_esc[pru])

print(f"Registros: {len(X)}  (entrenamiento {len(ent)}, prueba {len(pru)})")
print("\nPesos aprendidos:")
for nombre, peso in sorted(zip(nombres, modelo.w), key=lambda p: -abs(p[1])):
    print(f"  {nombre:<11} {peso:+.4f}")
print(f"  {'sesgo':<11} {modelo.b:+.4f}")

mse = ((y[pru] - y_pred) ** 2).mean()
print(f"\nMSE prueba:  {mse:.4f}")
print(f"RMSE prueba: {np.sqrt(mse):.4f}  (x $100,000)")
print(f"R2 prueba:   {r2(y[pru], y_pred):.4f}")

casa = X[pru][0]
precio = modelo.predecir(((casa - media) / desv).reshape(1, -1))[0]
print(f"\nEjemplo -> real: ${y[pru][0] * 100000:,.0f}   predicho: ${precio * 100000:,.0f}")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(modelo.historial)
ax[0].set_title("Costo por iteracion (descenso de gradiente)")
ax[0].set_xlabel("iteracion")
ax[0].set_ylabel("costo")

ax[1].scatter(y[pru], y_pred, s=4, alpha=0.4)
ax[1].plot([0, 5], [0, 5], "r--")
ax[1].set_title("Precio real vs predicho (prueba)")
ax[1].set_xlabel("real")
ax[1].set_ylabel("predicho")

plt.tight_layout()
plt.show()
