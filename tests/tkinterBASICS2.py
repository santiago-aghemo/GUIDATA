import tkinter as tk
from tkinter import messagebox

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text="MESSAGE", font=('Arial', 18))
        self.label.pack(padx=10,pady=10)

        self.tb = tk.Text(self.root, height=5, font=('Arial', 18))
        self.tb.bind('<KeyPress>',self.shortcut) #le asignamos un evento especifico a esta casilla de texto, en este caso vemos q tecla esta presionada y usamos una funcion para hacer algo
        self.tb.pack(padx=10,pady=10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text="SHOW MESSAGEBOX", font=('Arial',16), variable=self.check_state)
        #necesitamos una variable que tenga el valor de la checkbox
        self.check.pack(padx=10,pady=10)

        self.button = tk.Button(self.root, text="SHOW MESSAGE", font=('Arial',18), command=self.show_message)
        self.button.pack(padx=10,pady=10)

        self.root.mainloop()

    def show_message(self):
        if(self.check_state.get()==1):
            print(self.tb.get('1.0', tk.END))
            #Si queremos pasar el contenido de la textbox desde el comienzo hasta el final, debemos pasar
            #'1.0', el cual indica el comienzo, y tk.END() la cual marca el final
        else:
            messagebox.showinfo(title="Message", message="MARQUE LA CASILLA")
            #con messagebox podemos crear ventanas emergentes
    def shortcut(self,event):
        print(event)
        if(event.keysym=='Return'):
            messagebox.showinfo(title="TECLA", message="SE PRESIONO EL ENTER WOOO")
GUI()