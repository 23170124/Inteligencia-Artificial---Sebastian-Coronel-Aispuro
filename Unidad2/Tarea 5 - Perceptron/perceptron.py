import numpy as np
import matplotlib.pyplot as plt


class Perceptron:
    def __init__(self, tasa=0.1, max_epocas=100):
        self.tasa = tasa
        self.max_epocas = max_epocas

    def activacion(self, z):
        return np.where(z >= 0, 1, 0)

    def predecir(self, X):
        return self.activacion(X @ self.w + self.b)

    def entrenar(self, X, y):
        rng = np.random.default_rng(1)
        self.w = rng.uniform(-0.5, 0.5, X.shape[1])
        self.b = 0.0
        self.errores = []
        for epoca in range(self.max_epocas):
            fallos = 0
            for xi, yi in zip(X, y):
                delta = yi - self.predecir(xi)
                if delta != 0:
                    self.w += self.tasa * delta * xi
                    self.b += self.tasa * delta
                    fallos += 1
            self.errores.append(fallos)
            if fallos == 0:
                break
        return epoca + 1


# Ejemplo: aprobar o reprobar segun horas de estudio y horas de sueno
rng = np.random.default_rng(3)
aprobados = rng.normal([7.5, 7], 0.8, (40, 2))
reprobados = rng.normal([3, 3.5], 0.8, (40, 2))
X = np.vstack([aprobados, reprobados])
y = np.array([1] * 40 + [0] * 40)

p = Perceptron(tasa=0.1)
epocas = p.entrenar(X, y)
acierto = (p.predecir(X) == y).mean() * 100

print(f"Convergio en {epocas} epocas")
print(f"w = {np.round(p.w, 3)}   b = {p.b:.3f}")
print(f"Exactitud: {acierto:.1f}%")

for horas in ([8, 6], [2, 3], [5, 5]):
    r = p.predecir(np.array(horas))
    print(f"Estudio {horas[0]}h, sueno {horas[1]}h -> {'APRUEBA' if r else 'REPRUEBA'}")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].scatter(*aprobados.T, c="tab:green", label="aprueba")
ax[0].scatter(*reprobados.T, c="tab:red", label="reprueba")
xs = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 2)
# frontera: w0*x + w1*y + b = 0
ax[0].plot(xs, -(p.w[0] * xs + p.b) / p.w[1], "k--", label="frontera")
ax[0].set_xlabel("horas de estudio")
ax[0].set_ylabel("horas de sueno")
ax[0].legend()
ax[0].set_title("Frontera de decision")

ax[1].plot(range(1, len(p.errores) + 1), p.errores, marker="o")
ax[1].set_xlabel("epoca")
ax[1].set_ylabel("errores")
ax[1].set_title("Errores por epoca")

plt.tight_layout()
plt.show()
