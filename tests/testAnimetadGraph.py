import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

# ==== Leer los valores desde archivo ====
with open("dataForLiveGraph.txt", "r") as f:
    valores = [float(line.strip()) for line in f.readlines()]

# ==== Configuración inicial ====
ventana = tk.Tk()
ventana.title("Gráficos en Tiempo Real con Tkinter")
ventana.geometry("800x600")

# ==== Crear dos figuras y ejes ====
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

canvas1 = FigureCanvasTkAgg(fig1, master=ventana)
canvas1_widget = canvas1.get_tk_widget()
canvas1_widget.grid(row=0, column=0, sticky="nsew")

canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
canvas2_widget = canvas2.get_tk_widget()
canvas2_widget.grid(row=1, column=0, sticky="nsew")

# Hacer que las filas/columnas crezcan con la ventana
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_columnconfigure(0, weight=1)

# ==== Variables para graficado ====
xdata1, ydata1 = [], []
xdata2, ydata2 = [], []
counter = 0

# ==== Función que actualiza los gráficos ====
def actualizar(i):
    global xdata1, ydata1, xdata2, ydata2, counter

    xdata1.append(i + 1)
    ydata1.append(valores[i])
    xdata2.append(i + 1)
    ydata2.append(valores[i])
    counter += 1

    # Limpiar ejes y volver a graficar
    ax1.clear()
    ax2.clear()

    # Limitar ejes
    ax1.set_xlim(i - counter + 1, i + 1)
    ax2.set_xlim(i - counter + 1, i + 1)
    ax1.set_ylim(min(valores) - 5, max(valores) + 5)
    ax2.set_ylim(min(valores) - 5, max(valores) + 5)

    # Títulos opcionales
    ax1.set_title("Gráfico 1")
    ax2.set_title("Gráfico 2")

    # Dibujar
    ax1.plot(xdata1, ydata1, 'b-o')
    ax2.plot(xdata2, ydata2, 'r-o')

    canvas1.draw()
    canvas2.draw()

    # Si ya hay 30 valores, reiniciamos
    if counter == 30:
        xdata1.clear()
        ydata1.clear()
        xdata2.clear()
        ydata2.clear()
        counter = 0

# ==== Loop de animación ====
def loop():
    for i in range(len(valores)):
        actualizar(i)
        ventana.update()
        time.sleep(0.01)  # ajustá la velocidad si querés

    print("Finalizado.")

# ==== Ejecutar loop después de iniciar ventana ====
ventana.after(100, loop)
ventana.mainloop()
