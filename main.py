#La idea que tengo ahora mismo es crear un grid. en cada fila vas a poder encontrar en la primera
#columna el plotting "en vivo" de la variable, junto a un contador que muestra, actualizandose
#constantemente el valor de la variable
#
#ideas: lo mas facil supongo seria comenzar que el programa apenas se ejecuta comienza a leer, y a
#grabar, pq tambien va a ir guardando en un docuemnto de texto lo que vaya recopilando. Pero me gustaria
#poder "delegar" estas funciones a botones, asi el usuario decide cuando comienza una nueva grabacion de
#datos. Con una funcion "write" cada vez que se presiona el boton para que comience a copiar lo que lea
#del monitor serie deberia bastar. creo que un archivo nuevo cada vez que se ejecute la funcion no sera 
#tanto problema. tampoco voy a codear que continue desde donde estaba si es que se corto a la mitad
#
#otra cuestion importante: leer monitor serie. al parecer es perfectamente posible. RECORDATORIO: probar el codigo
#con un solo sensor con el arduino. si funciona con un sensor deberia funcionar con todos, solo hace falta agregarlos
#a la grid


import tkinter as tk #tkinter, las ventanas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #esto es para convertir lo de matplot a tkinter
import matplotlib.pyplot as plt #funciones para plotear
import numpy as np #numpy, para tener funciones matematicas
import time


root = tk.Tk() #este es la base de todo, sobre esta ventana van a estar todos los componentes

root.geometry("1000x1000")#dimensiones

dataGRID = tk.Frame(root)
dataGRID.columnconfigure(0,weight=1)
dataGRID.columnconfigure(1,weight=1)#con el weight tanto en la columna como en la fila, en este caso cada celda va a ocupar 1/4 del espacio
dataGRID.rowconfigure(0,weight=1)
#dataGRID.rowconfigure(1,weight=1)

#esto sirve mas que nada para cuando ajustas el tamaño de la ventana


l1 = tk.Label(dataGRID)
l1.grid(row=0, column=0, sticky='nsew')
l11 = tk.Label(dataGRID,text="SENO", font=('Arial',16))
l11.grid(row=0,column=0, sticky='n')

l2 = tk.Label(dataGRID)
l2.grid(row=0, column=1, sticky='nsew')
l22 = tk.Label(dataGRID,text="COSENO", font=('Arial',16))
l22.grid(row=0,column=1, sticky='n')

'''
l3 = tk.Label(dataGRID)
l3.grid(row=1, column=0, sticky='nsew')
l33 = tk.Label(dataGRID,text="TANGETE", font=('Arial',16))
l33.grid(row=1,column=0, sticky='n')

l4 = tk.Label(dataGRID)
l4.grid(row=1, column=1, sticky='nsew')
l44 = tk.Label(dataGRID,text="ARCOTANGETE", font=('Arial',16))
l44.grid(row=1,column=1, sticky='n')
'''

fig1,ax1 = plt.subplots()
x1 = np.linspace(0,2*np.pi,100)
ax1.plot(x1,np.sin(x1))
canva1 = FigureCanvasTkAgg(fig1,master=l1)
canva1.draw()
canva1.get_tk_widget().pack()

'''
fig2,ax2 = plt.subplots()
x2 = np.linspace(0,2*np.pi,100)
ax2.plot(x2,np.cos(x2))
canva2 = FigureCanvasTkAgg(fig2,master=l2)
canva2.draw()
canva2.get_tk_widget().pack()

fig3,ax3 = plt.subplots()
x3 = np.linspace(0,2*np.pi,100)
ax3.plot(x3,np.tan(x3))
canva3 = FigureCanvasTkAgg(fig3,master=l3)
canva3.draw()
canva3.get_tk_widget().pack()

fig4,ax4 = plt.subplots()
x4 = np.linspace(0,2*np.pi,100)
ax4.plot(x4,np.arctan(x4))
canva4 = FigureCanvasTkAgg(fig4,master=l4)
canva4.draw()
canva4.get_tk_widget().pack()
'''

dataGRID.pack(fill='both', expand=True)
root.mainloop()