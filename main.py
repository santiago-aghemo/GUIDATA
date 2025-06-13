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
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #esto es para convertir lo de matplot a tkinter
import matplotlib.pyplot as plt #funciones para plotear
import matplotlib
import numpy as np #numpy, para tener funciones matematicas
import time
import serial #leer monitor serie

#estilo del matplot
matplotlib.rcParams.update({
    'axes.facecolor': '#2e2e2e',
    'axes.edgecolor': '#ffffff',
    'axes.labelcolor': '#ffffff',
    'figure.facecolor': '#2e2e2e',
    'xtick.color': '#ffffff',
    'ytick.color': '#ffffff',
    'text.color': '#ffffff',
    'axes.titlecolor': '#ffffff'
})

class GUI:
    def __init__(self,port='COM3', baudrate=9600):
        

        self.grabarStatus = 0
        self.nombreArchivo = None
        self.root = tk.Tk() #este es la base de todo, sobre esta ventana van a estar todos los componentes
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.root.configure(bg="#1e1e1e")

        #configuramos el cronometro
        self.inicio = time.time()
        self.Cronometro = tk.Label(self.root, text="00:00.000", font=('Lucida Console', 25), bg="#1e1e1e", fg="#ffffff")
        self.Cronometro.pack()

        self.actualizarTime()

        #estilo de ttk personalizado
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure("TButton",
                             background="#444",
                             foreground="#fff",
                             font=('Lucida Console', 12),
                             padding=10)
        self.style.map("TButton",
                       background=[("active", "#666"), ("pressed", "#222")])
        

        #configuracion de la tabla que va a mostrar los datos
        self.dataGRID=tk.Frame(self.root, bg="#1e1e1e")
        self.dataGRID.columnconfigure(0,weight=1)
        self.dataGRID.columnconfigure(1,weight=10)
        self.dataGRID.columnconfigure(2, weight=5)
        self.dataGRID.rowconfigure(0, weight=1)
        self.dataGRID.rowconfigure(1, weight=1)


        self.g1 = tk.Label(self.dataGRID, bg="#1e1e1e")
        self.g1.grid(row=0, column=1, sticky='nsew')
        
        self.g2 = tk.Label(self.dataGRID, bg="#1e1e1e")
        self.g2.grid(row=1, column=1, sticky='nsew')


        self.d1T = tk.Label(self.dataGRID, text="Tiempo del pulso", font=('Lucida Console', 25), bg="#1e1e1e", fg="#ffffff")
        self.d1T.grid(row=0, column=0, sticky='nsew')
        
        self.d1 = tk.Label(self.dataGRID, text=" ", font=('Lucida Console', 25), bg="#1e1e1e", fg="#00ffcc")
        self.d1.grid(row=0, column=2, sticky='nsew')

        self.d1D = tk.Label(self.dataGRID, text="DATO ACTUAL", bg="#1e1e1e", fg="#ccc", font=("Lucida Console", 20, "bold"))
        self.d1D.grid(row=0, column=2, sticky='n')


        self.d2T = tk.Label(self.dataGRID, text="Distancia Medida", font=('Lucida Console', 25), bg="#1e1e1e", fg="#ffffff")
        self.d2T.grid(row=1, column=0, sticky='nsew')

        self.d2 = tk.Label(self.dataGRID, text=" ", font=('Lucida Console', 25), bg="#1e1e1e", fg="#00ffcc")
        self.d2.grid(row=1, column=2, sticky='nsew')

        self.d2D = tk.Label(self.dataGRID, text="DATO ACTUAL", bg="#1e1e1e", fg="#ccc", font=("Lucida Console", 20, "bold"))
        self.d2D.grid(row=1, column=2, sticky='n')

        self.botonFrame = tk.Frame(self.root, bg="#1e1e1e")
        self.botonFrame.pack(pady=10)

        #vamos a hacer los botones para iniciar/parar la grabacion de datos
        self.bR=tk.Button(self.botonFrame, text="GRABAR", font=('Lucida Console', 16), command=lambda: self.iniciar_grabar(f"session_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"))
        self.bR.pack(side="left", pady=5)

        self.bS=tk.Button(self.botonFrame, text="STOP", font=('Lucida Console', 16), command=self.parar_grabacion)
        self.bS.pack(side="left", pady=5)


        self.xdata1, self.yadata1 = [],[]
        self.xdata2, self.yadata2 = [],[] #iniciamos los datos de x e y ambos en cero
        self.counter=0

        #creamos el grafico 1
        self.fig1,self.ax1 = plt.subplots()
        self.ax1.plot(self.counter,float(0))
        self.canva1 = FigureCanvasTkAgg(self.fig1,master=self.g1)
        self.canva1.draw()
        self.canva1.get_tk_widget().pack(fill='both', expand=True)
        
        #creamos el grafico 2
        self.fig2,self.ax2 = plt.subplots()
        self.ax2.plot(self.counter, float(0))
        self.canva2 = FigureCanvasTkAgg(self.fig2,master=self.g2)
        self.canva2.draw()
        self.canva2.get_tk_widget().pack(fill='both', expand=True)
        
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

        
        #timepo actual
        timepo_actual = time.time()-self.inicio

        #------------------ACTUALIZACION Y DETALLES DEL GRAFICO 1-----------------------------------
        self.xdata1.append(timepo_actual)#agregamos a los valores de x el segundo actual(counter)
        self.yadata1.append(tiempoPulso)#agregamos el ultimo valor leido del monitor serie a los valores de y
        self.ax1.clear()#limpiamos los valores actuales
        
        '''
        #esto es para mantener el grafico siempre mostrando una porcion pequeña de datos(viejo)
        if self.counter < 30:
            self.ax1.set_xlim(1, 30)
        else:
            self.ax1.set_xlim(self.counter - 29, self.counter)
        '''

        self.ax1.set_xlim(max(0, self.xdata1[-1]-30), self.xdata1[-1]+1)#aca hice una modificacion del ajuste este que "mostraba siempre 30"
        #ahora se va corriendo el cuadro, pero mantiene tambien la relacion del contador con el eje de las x: cuando el contador marca 20, en el eje de las x se marca 20

        #titulo del grafico
        self.ax1.set_title("GRAFICO", fontdict={"fontsize": 14, "fontweight": "bold", "family": "Lucida Console"})
        #nombres a los ejes
        self.ax1.set_xlabel("Segundos", fontdict={"fontsize": 14, "fontweight": "bold", "family": "Lucida Console"})
        #trazamos el grafico
        self.ax1.plot(self.xdata1, self.yadata1, '-', color='#00ffff')
        self.ax1.grid(True, linestyle='--', linewidth=0.5, color='#888')
        self.canva1.draw()

        self.ax1.relim()
        self.ax1.autoscale_view()

        #------------------ACTUALIZACION Y DETALLES DEL GRAFICO 2-----------------------------------
        self.xdata2.append(timepo_actual)#agregamos a los valores de x el segundo actual(counter)
        self.yadata2.append(dstMedida)#agregamos el ultimo valor leido del monitor serie a los valores de y
        self.ax2.clear()#limpiamos los valores actuales

        '''
        #esto es para mantener el grafico siempre mostrando una porcion pequeña de datos(viejo)
        if self.counter < 30:
            self.ax2.set_xlim(1, 30)
        else:
            self.ax2.set_xlim(self.counter - 29, self.counter)
        '''
        self.ax2.set_xlim(max(0, self.xdata2[-1]-30), self.xdata2[-1]+1)#ajuste asi el contador va al mismo ritmo que el cuadro

        #titulo del grafico
        self.ax2.set_title("GRAFICO", fontdict={"fontsize": 14, "fontweight": "bold", "family": "Lucida Console"})
        #nombres a los ejes
        self.ax2.set_xlabel("Segundos", fontdict={"fontsize": 14, "fontweight": "bold", "family": "Lucida Console"})
        self.ax2.set_ylabel("Distancia", fontdict={"fontsize": 14, "fontweight": "bold", "family": "Lucida Console"})
        #trazamos el grafico
        self.ax2.plot(self.xdata2, self.yadata2, '-', color='#ff00aa')
        self.ax2.grid(True, linestyle='--', linewidth=0.5, color='#888')
        self.canva2.draw()

        self.ax2.relim()
        self.ax2.autoscale_view()

        self.counter+=1#sumamos uno al contador 

        #actualizar el valor mostrado en vivo
        self.d1.config(text=str(tiempoPulso))
        self.d2.config(text=str(dstMedida))

        if(self.grabarStatus):#chequear si se inicio grabacion
            self.grabar(valueRAW)#grabar dato
        
        self.root.after(1000,self.actualizar)#repetir cada 1 segundo

    def iniciar_grabar(self,path):#iniciar la grabacion y definir el nombre del archivo de la sesion actual
        if(self.grabarStatus==0):
            with open(path, 'w') as archivo:
                archivo.write(str(round(time.time()-self.inicio, 3))+': '+str(self.ser.readline().decode().strip())+'\n')
            self.nombreArchivo = path
            self.grabarStatus=1
        else:#si ya se inicio una grabacion, alertar al usuario
            messagebox.showinfo(message="YA SE HA INICIADO UNA GRABACION")

    def grabar(self, value):#grabar dato actual
        with open(self.nombreArchivo,'a') as archivo:
            archivo.write(str(round(time.time()-self.inicio, 3))+': '+str(value)+'\n')

    def parar_grabacion(self):#cortar la grabacion
        self.nombreArchivo = None
        self.grabarStatus=0

    def actualizarTime(self):
        timepo_actual = time.time()-self.inicio

        minutos = int(timepo_actual//60)
        segundos = int(timepo_actual%60)
        milesimas = int((timepo_actual-int(timepo_actual)) * 1000)

        self.Cronometro.config(text=f"{minutos:02}:{segundos:02}.{milesimas:03}")
        self.root.after(10, self.actualizarTime)
        
GUI()