import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

# ==== Leer los valores desde archivo ====
with open("dataForLiveGraph.txt", "r") as f:
    valores = [float(line.strip()) for line in f.readlines()]

ventana = tk.Tk()
ventana.title("Gráficos en Tiempo Real con Tkinter")
ventana.geometry("800x600")

# ==== Crear figuras ====
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

canvas1 = FigureCanvasTkAgg(fig1, master=ventana)
canvas1_widget = canvas1.get_tk_widget()
canvas1_widget.grid(row=0, column=0, sticky="nsew")

canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
canvas2_widget = canvas2.get_tk_widget()
canvas2_widget.grid(row=1, column=0, sticky="nsew")

ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)

# ==== Datos ====
xdata1, ydata1 = [], []
xdata2, ydata2 = [], []

# ==== Actualización ====
def actualizar(i):
    x = i + 1
    y = valores[i]

    xdata1.append(x)
    ydata1.append(y)
    xdata2.append(x)
    ydata2.append(y)

    ax1.clear()
    ax2.clear()

    # Ventana X siempre fija en 30 valores
    if x < 30:
        ax1.set_xlim(1, 30)
        ax2.set_xlim(1, 30)
    else:
        ax1.set_xlim(x - 29, x)
        ax2.set_xlim(x - 29, x)

    ax1.set_ylim(min(valores) - 5, max(valores) + 5)
    ax2.set_ylim(min(valores) - 5, max(valores) + 5)

    ax1.set_title("Gráfico 1")
    ax2.set_title("Gráfico 2")

    ax1.plot(xdata1, ydata1, 'b-o')
    ax2.plot(xdata2, ydata2, 'r-o')

    canvas1.draw()
    canvas2.draw()

# ==== Loop ====
def loop():
    for i in range(len(valores)):
        actualizar(i)
        ventana.update()
        time.sleep(0.1)

    print("Finalizado.")

ventana.after(100, loop)
ventana.mainloop()
