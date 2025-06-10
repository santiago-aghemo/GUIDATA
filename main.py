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
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #esto es para convertir lo de matplot a tkinter
import matplotlib.pyplot as plt #funciones para plotear
import numpy as np #numpy, para tener funciones matematicas
import time
import serial #leer monitor serie


class GUI:
    def __init__(self,port='COM3', baudrate=9600):
        self.grabarStatus = 0
        self.nombreArchivo = None
        self.root = tk.Tk() #este es la base de todo, sobre esta ventana van a estar todos los componentes
        #self.root.geometry('1000x1000')
        self.ser = serial.Serial(port=port, baudrate=baudrate)

        #configuracion de la tabla que va a mostrar los datos
        self.dataGRID=tk.Frame(self.root)

        self.dataGRID.columnconfigure(0,weight=3)
        self.dataGRID.columnconfigure(1,weight=1)
        self.dataGRID.rowconfigure(0, weight=1)
        self.dataGRID.rowconfigure(1, weight=1)


        self.g1=tk.Label(self.dataGRID)
        self.g1.grid(row=0,column=0,sticky='nsew')
        
        self.g2=tk.Label(self.dataGRID)
        self.g2.grid(row=1, column=0, sticky='nsew')


        self.d1=tk.Label(self.dataGRID,text=" ", font=('Arial',16))
        self.d1.grid(row=0,column=1,sticky='nsew')

        self.d1T=tk.Label(self.dataGRID,text="DATO ACTUAL")
        self.d1T.grid(row=0,column=1, sticky='n')

        self.d2=tk.Label(self.dataGRID,text=" ", font=('Arial',16))
        self.d2.grid(row=1,column=1,sticky='nsew')

        self.d2T=tk.Label(self.dataGRID,text="DATO ACTUAL")
        self.d2T.grid(row=1,column=1,sticky='n')

        #vamos a hacer los botones para iniciar/parar la grabacion de datos
        self.bR=tk.Button(self.root, text="GRABAR", font=('Arial', 16), command=lambda: self.iniciar_grabar(f"session_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt", time.strftime('%Y-%m-%d_%H-%M-%S')))
        self.bR.pack(anchor='sw')
        
        self.bS=tk.Button(self.root, text="STOP", font=('Arial', 16), command=self.parar_grabacion)
        self.bS.pack(anchor='sw')
        self.xdata1, self.yadata1 = [],[]
        self.xdata2, self.yadata2 = [],[] #iniciamos los datos de x e y ambos en cero
        self.counter=0

        #creamos el grafico 1
        self.fig1,self.ax1 = plt.subplots()
        self.ax1.plot(self.counter,float(0))
        self.canva1 = FigureCanvasTkAgg(self.fig1,master=self.g1)
        self.canva1.draw()
        self.canva1.get_tk_widget().pack()
        
        #creamos el grafico 2
        self.fig2,self.ax2 = plt.subplots()
        self.ax2.plot(self.counter, float(0))
        self.canva2 = FigureCanvasTkAgg(self.fig2,master=self.g2)
        self.canva2.draw()
        self.canva2.get_tk_widget().pack()
        
        self.actualizar()
        self.dataGRID.pack(fill='both',expand=True)
        self.root.mainloop()

    def actualizar(self):

        #actualizar grafico
        valueRAW=self.ser.readline().decode().strip()#leer monitor serie
        valorS=str(valueRAW)#pasar valores del monitor serie a float
        valueTIME=str(time.strftime('%Y-%m-%d_%H-%M-%S'))#registramos cuando llego el valor

        #extraemos los datos del raw
        partes = valorS.split()
        tiempoPulso = float(partes[0])
        dstMedida = float(partes[1])

        


        #------------------ACTUALIZACION Y DETALLES DEL GRAFICO 1-----------------------------------
        self.xdata1.append(self.counter)#agregamos a los valores de x el segundo actual(counter)
        self.yadata1.append(tiempoPulso)#agregamos el ultimo valor leido del monitor serie a los valores de y

        self.ax1.clear()#limpiamos los valores actuales

        #esto es para mantener el grafico siempre mostrando una porcion pequeña de datos
        if self.counter < 30:
            self.ax1.set_xlim(1, 30)
        else:
            self.ax1.set_xlim(self.counter - 29, self.counter)

        #titulo del grafico
        self.ax1.set_title("GRAFICO")
        #nombres a los ejes
        self.ax1.set_xlabel("Segundos")

        #trazamos el grafico
        self.ax1.plot(self.xdata1,self.yadata1,'b-o')

        self.canva1.draw()

        #------------------ACTUALIZACION Y DETALLES DEL GRAFICO 2-----------------------------------
        self.xdata2.append(self.counter)#agregamos a los valores de x el segundo actual(counter)
        self.yadata2.append(dstMedida)#agregamos el ultimo valor leido del monitor serie a los valores de y

        self.ax2.clear()#limpiamos los valores actuales

        #esto es para mantener el grafico siempre mostrando una porcion pequeña de datos
        if self.counter < 30:
            self.ax2.set_xlim(1, 30)
        else:
            self.ax2.set_xlim(self.counter - 29, self.counter)

        #titulo del grafico
        self.ax2.set_title("GRAFICO")
        #nombres a los ejes
        self.ax2.set_xlabel("Segundos")

        #trazamos el grafico
        self.ax2.plot(self.xdata2,self.yadata2,'b-o')

        self.canva2.draw()

        self.counter+=1#sumamos uno al contador 

        #actualizar el valor mostrado en vivo
        self.d1.config(text=str(tiempoPulso))
        self.d2.config(text=str(dstMedida))

        if(self.grabarStatus):#chequear si se inicio grabacion
            self.grabar(valueRAW,valueTIME)#grabar dato
        
        self.root.after(1000,self.actualizar)#repetir cada 1 segundo

    def iniciar_grabar(self,path,time):#iniciar la grabacion y definir el nombre del archivo de la sesion actual
        if(self.grabarStatus==0):
            with open(path, 'w') as archivo:
                archivo.write(time+': '+str(self.ser.readline().decode().strip())+'\n')
            self.nombreArchivo = path
            self.grabarStatus=1
        else:#si ya se inicio una grabacion, alertar al usuario
            messagebox.showinfo(message="YA SE HA INICIADO UNA GRABACION")

    def grabar(self, value,time):#grabar dato actual
        with open(self.nombreArchivo,'a') as archivo:
            archivo.write(time+': '+str(value)+'\n')

    def parar_grabacion(self):#cortar la grabacion
        self.nombreArchivo = None
        self.grabarStatus=0
        
GUI()