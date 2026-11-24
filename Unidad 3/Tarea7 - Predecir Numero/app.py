from pathlib import Path
import tkinter as tk

import joblib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

RUTA_MODELO = Path(__file__).parent / "modelo_mnist.joblib"
LADO = 300
PINCEL = 22


def a_formato_mnist(img):
    caja = img.getbbox()
    if caja is None:
        return None
    digito = img.crop(caja)
    w, h = digito.size
    f = 20 / max(w, h)
    digito = digito.resize((max(1, int(w * f)), max(1, int(h * f))), Image.LANCZOS)

    lienzo = Image.new("L", (28, 28), 0)
    lienzo.paste(digito, ((28 - digito.width) // 2, (28 - digito.height) // 2))
    arr = np.asarray(lienzo.filter(ImageFilter.GaussianBlur(0.5)), dtype=np.float32) / 255.0

    # MNIST centra cada numero por su centro de masa
    filas, cols = np.indices(arr.shape)
    total = arr.sum()
    dy = int(round(14 - (filas * arr).sum() / total))
    dx = int(round(14 - (cols * arr).sum() / total))
    arr = np.roll(np.roll(arr, dy, axis=0), dx, axis=1)
    return arr.reshape(1, -1)


class App:
    def __init__(self, raiz, modelo):
        self.modelo = modelo
        self.previo = None
        raiz.title("Tarea 7 - Predecir numero")

        self.lienzo = tk.Canvas(raiz, width=LADO, height=LADO, bg="black", cursor="pencil")
        self.lienzo.grid(row=0, column=0, rowspan=2, padx=12, pady=12)
        self.lienzo.bind("<B1-Motion>", self.trazar)
        self.lienzo.bind("<ButtonRelease-1>", self.soltar)

        self.resultado = tk.Label(raiz, text="?", font=("Segoe UI", 64, "bold"), width=3)
        self.resultado.grid(row=0, column=1, padx=12)

        self.barras = tk.Canvas(raiz, width=240, height=LADO - 110)
        self.barras.grid(row=1, column=1, padx=12)

        tk.Button(raiz, text="Borrar", width=14, command=self.borrar).grid(
            row=2, column=0, columnspan=2, pady=(0, 12))

        self.borrar()

    def trazar(self, e):
        if self.previo:
            self.lienzo.create_line(*self.previo, e.x, e.y, fill="white",
                                    width=PINCEL, capstyle=tk.ROUND, smooth=True)
            self.pincel.line([self.previo, (e.x, e.y)], fill=255, width=PINCEL)
        r = PINCEL // 2
        self.pincel.ellipse([e.x - r, e.y - r, e.x + r, e.y + r], fill=255)
        self.previo = (e.x, e.y)

    def soltar(self, _):
        self.previo = None
        self.predecir()

    def predecir(self):
        x = a_formato_mnist(self.imagen)
        if x is None:
            return
        probs = self.modelo.predict_proba(x)[0]
        self.resultado.config(text=str(int(probs.argmax())))
        self.dibujar_barras(probs)

    def dibujar_barras(self, probs):
        self.barras.delete("all")
        alto = (LADO - 110) / 10
        for d, p in enumerate(probs):
            y = d * alto
            color = "#2e86de" if d == probs.argmax() else "#b0b0b0"
            self.barras.create_text(12, y + alto / 2, text=str(d))
            self.barras.create_rectangle(28, y + 3, 28 + p * 170, y + alto - 3, fill=color, width=0)
            self.barras.create_text(205, y + alto / 2, text=f"{p * 100:.0f}%", anchor="w")

    def borrar(self):
        self.lienzo.delete("all")
        self.barras.delete("all")
        self.resultado.config(text="?")
        self.imagen = Image.new("L", (LADO, LADO), 0)
        self.pincel = ImageDraw.Draw(self.imagen)


if not RUTA_MODELO.exists():
    raise SystemExit("Primero corre entrenar.py para generar modelo_mnist.joblib")

raiz = tk.Tk()
App(raiz, joblib.load(RUTA_MODELO))
raiz.mainloop()
