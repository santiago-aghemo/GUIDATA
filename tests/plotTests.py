import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def actualizar_grafico1():
    ax.clear()
    y = np.cos(x)
    ax.plot(x, y, color='red')
    ax.set_title("Coseno de x")
    canvas.draw()
def actualizar_grafico2():
    ax.clear()
    y = np.sin(x)
    ax.plot(x, y, color='red')
    ax.set_title("Coseno de x")
    canvas.draw()
def actualizar_grafico3():
    ax.clear()
    y = np.tan(x)
    ax.plot(x, y, color='red')
    ax.set_title("Coseno de x")
    canvas.draw()

root = tk.Tk()
root.title("Gráfico interactivo")

fig, ax = plt.subplots() #fig es el "lienzo" y ax es el grafico. usando subplots() te permite modificarle otras variables
x = np.linspace(0, 2*np.pi, 100)#x va de 0 a 2 pi, con 100 puntos
ax.plot(x, np.sin(x))
canvas = FigureCanvasTkAgg(fig, master=root)#aca le pasas el grafico de matplot a tkinter
canvas.draw()
canvas.get_tk_widget().pack()

btn = tk.Button(root, text="Cambiar a Coseno", command=actualizar_grafico1)
btn.pack()
btn2 = tk.Button(root, text="Cambiar a Seno", command=actualizar_grafico2)
btn2.pack()
btn3 = tk.Button(root, text="Cambiar a Tangente", command=actualizar_grafico3)
btn3.pack()
root.mainloop()
