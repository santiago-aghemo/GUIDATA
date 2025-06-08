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
import serial #leer monitor serie

class GUI:
    def __init__(self,port='COM3', baudrate=9600):
        self.root = tk.Tk() #este es la base de todo, sobre esta ventana van a estar todos los componentes
        self.ser = serial.Serial(port=port, baudrate=baudrate)

        #configuracion de la tabla que va a mostrar los datos
        self.dataGRID=tk.Frame(self.root)

        self.dataGRID.columnconfigure(0,weight=1)
        self.dataGRID.columnconfigure(1,weight=1)
        self.dataGRID.rowconfigure(0,weight=1)

        self.l1=tk.Label(self.dataGRID)
        self.l1.grid(row=0,column=0,sticky='nsew')

        self.l2=tk.Label(self.dataGRID, text=str(self.ser.readline().decode().strip()), font=('Arial',16))
        self.l2.grid(row=0,column=1,sticky='nsew')
        self.l2T=tk.Label(self.dataGRID,text="DATO ACTUAL")
        self.l2T.grid(row=0,column=1, sticky='n')
        
        self.xdata, self.yadata = [],[] #iniciamos los datos de x e y ambos en cero
        self.counter=0

        #creamos el grafico
        self.fig1,self.ax1 = plt.subplots()
        self.ax1.plot(self.counter,float(self.ser.readline().decode().strip()))
        self.canva1 = FigureCanvasTkAgg(self.fig1,master=self.root)
        self.canva1.draw()
        self.canva1.get_tk_widget().pack()
        

        
        self.actualizar()
        self.dataGRID.pack(fill='both', expand=True)
        self.root.mainloop()

    def actualizar(self):

        #actualizar grafico
        valueRAW=self.ser.readline().decode().strip()#leer monitor serie
        valorF=float(valueRAW)#pasar valores del monitor serie a float

        self.xdata.append(self.counter)#agregamos a los valores de x el segundo actual(counter)
        self.yadata.append(valorF)#agregamos el ultimo valor leido del monitor serie a los valores de y

        self.ax1.clear()#limpiamos los valores actuales

        #esto es para mantener el grafico siempre mostrando una porcion pequeña de datos
        if self.counter < 30:
            self.ax1.set_xlim(1, 30)
        else:
            self.ax1.set_xlim(self.counter - 29, self.counter)

        #titulo del grafico
        self.ax1.set_title("GRAFICO")

        #trazamos el grafico
        self.ax1.plot(self.xdata,self.yadata,'b-o')

        self.canva1.draw()

        self.counter+=1#sumamos uno al contador 

        #actualizar el valor mostrado en vivo
        self.l2.config(text=str(valueRAW))

        #self.dataGRID.pack(fill='both', expand=True)
       
        self.root.after(1000,self.actualizar)#repetir cada 1 segundo


GUI()