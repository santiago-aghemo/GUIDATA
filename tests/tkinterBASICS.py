import tkinter as tk


w1 = tk.Tk()#inicializamos esta variable como una ventana

w1.geometry("500x500")#aca definimos las dimensiones de la ventana
w1.title("WINDOW1")#aca ponemos titulo


#configuramos una etiqueta que muestre un texto
#podemos determinar sobre que ventana va a estar esta etiqueta
#podemos determinar la fuente y el tamaño
#podemos determinar "padding", separacion con respecto a los bordes de la ventana
label = tk.Label(w1, text="Hello World!", font=('Arial',18))
label.pack(padx=20, pady=20)

#casilla de texto, permite meter texto
textbox = tk.Text(w1, height=3, font=('Arial',16))
textbox.pack(padx=10, pady=10)

bf = tk.Frame(w1)#grilla
bf.columnconfigure(0,weight=1)#agregamos columnas
bf.columnconfigure(1,weight=1)
bf.columnconfigure(2,weight=1)

b1 = tk.Button(bf, text="1", font=('Arial',18))
b1.grid(row=0, column=0, sticky=tk.W+tk.E)#con el sticky cada celda va a estar pegada a la otra (ver diseño de la calculadora de windows)

b2 = tk.Button(bf, text="2", font=('Arial',18))
b2.grid(row=0, column=1, sticky=tk.W+tk.E)

b3 = tk.Button(bf, text="3", font=('Arial',18))
b3.grid(row=0, column=2, sticky=tk.W+tk.E)

b4 = tk.Button(bf, text="4", font=('Arial',18))
b4.grid(row=1, column=0, sticky=tk.W+tk.E)

b6 = tk.Button(bf, text="5", font=('Arial',18))
b6.grid(row=1, column=1, sticky=tk.W+tk.E)

b7 = tk.Button(bf, text="6", font=('Arial',18))
b7.grid(row=1, column=2, sticky=tk.W+tk.E)

bf.pack(fill='x')#se va a pegar a los bordes de la ventana

boton = tk.Button(w1, text="TEST")
boton.place(x=200, y=350, height=100, width=100)#ponemos el boton de una forma mas "precisa"

#button = tk.Button(w1, text="click me", font=('Arial', 18))
#button.pack(padx=10, pady=10)

#este tipo de casilla de texto no permite saltos de lineas y tiene un tamaño fijo 
#myentry = tk.Entry(w1)
#myentry.pack()

w1.mainloop()#y aca la abrimos indefinidamente
