import tkinter as tk

root = tk.Tk()
root.geometry("300x200")  # Ventana de tamaño fijo

# Etiqueta arriba a la izquierda
label1 = tk.Label(root, text="NW", bg="lightblue")
label1.pack(anchor="nw", padx=5, pady=5)

# Etiqueta arriba a la derecha
label2 = tk.Label(root, text="NE", bg="lightgreen")
label2.pack(anchor="ne", padx=5, pady=5)

# Etiqueta centrada
label3 = tk.Label(root, text="CENTER", bg="lightpink")
label3.pack(anchor="center", padx=5, pady=5)

# Etiqueta abajo al medio
label4 = tk.Label(root, text="S", bg="lightgray")
label4.pack(anchor="s", padx=5, pady=5)

root.mainloop()
