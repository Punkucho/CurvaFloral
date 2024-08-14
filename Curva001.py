import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from random import randint
import os

# Diccionario para almacenar los datos de avistamientos y colores
avistamientos = {mes: [0, 0] for mes in range(12)}  # Cada mes tiene dos quincenas y cuenta de plantas
colores = {}
plantas_avistadas = {}

# Función para generar un color aleatorio en formato hexadecimal
def generar_color():
    return "#{:06x}".format(randint(0, 0xFFFFFF))

# Función para agregar datos y mostrar un mensaje de confirmación
def agregar_avistamiento():
    planta = planta_entry.get()
    if not planta:
        messagebox.showerror("Error", "Debe ingresar el nombre de la planta.")
        return
    
    if planta not in colores:
        colores[planta] = generar_color()
    
    meses_avistados = []
    for mes in range(12):
        if quincenas[mes][0].get() == 1 or quincenas[mes][1].get() == 1:
            if planta not in plantas_avistadas:
                plantas_avistadas[planta] = []
            if mes not in plantas_avistadas[planta]:
                plantas_avistadas[planta].append(mes)
                meses_avistados.append(meses[mes])
            if quincenas[mes][0].get() == 1:
                avistamientos[mes][0] += 1
            if quincenas[mes][1].get() == 1:
                avistamientos[mes][1] += 1

    if planta in plantas_avistadas:
        actualizar_lista_plantas(planta)

    messagebox.showinfo("Éxito", f"Avistamiento de {planta} registrado.")
    planta_entry.delete(0, tk.END)
    for mes in range(12):
        quincenas[mes][0].set(0)
        quincenas[mes][1].set(0)

# Función para actualizar la lista de plantas avistadas
def actualizar_lista_plantas(planta):
    lista_plantas.delete(0, tk.END)
    for planta, meses in plantas_avistadas.items():
        meses_texto = ", ".join(meses[mes] for mes in meses)
        lista_plantas.insert(tk.END, f"{planta} (Meses: {meses_texto})")
        lista_plantas.itemconfig(tk.END, {'fg': colores[planta]})

# Función para crear y mostrar el gráfico en una nueva ventana
def mostrar_grafico():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Crear la nueva ventana para el gráfico
    grafico_ventana = tk.Toplevel(root)
    grafico_ventana.title("Generador de curva floral")

    # Frame para contener el gráfico y el scrollbar
    grafico_frame = ttk.Frame(grafico_ventana)
    grafico_frame.pack(fill=tk.BOTH, expand=True)
    
    # Crear un scrollbar vertical y horizontal
    scrollbar_y = tk.Scrollbar(grafico_frame, orient=tk.VERTICAL)
    scrollbar_x = tk.Scrollbar(grafico_frame, orient=tk.HORIZONTAL)

    # Crear un canvas donde se colocará el gráfico
    grafico_canvas = tk.Canvas(grafico_frame, scrollregion=(0, 0, 800, 600),
                               yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.config(command=grafico_canvas.yview)
    scrollbar_x.config(command=grafico_canvas.xview)

    # Empaquetar scrollbars y canvas
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    grafico_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.set_title("Generador de curva floral")
    ax.set_xlabel('Meses')
    ax.set_ylabel('Cantidad de Plantas')
    
    for mes in range(12):
        if avistamientos[mes][0] > 0:
            ax.scatter(meses[mes], avistamientos[mes][0], color="blue", label=f"{meses[mes]} - 1ra Quincena" if mes == 0 else "")
        if avistamientos[mes][1] > 0:
            ax.scatter(meses[mes], avistamientos[mes][1], color="red", label=f"{meses[mes]} - 2da Quincena" if mes == 0 else "")

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Quincenas")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=grafico_canvas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Función para ajustar el tamaño del gráfico al redimensionar la ventana
    def on_resize(event):
        fig.set_size_inches(event.width / 100, event.height / 100)
        canvas.draw()

    grafico_ventana.bind("<Configure>", on_resize)

    # Botón para guardar el gráfico dentro de la ventana del gráfico
    btn_guardar = ttk.Button(grafico_ventana, text="Guardar Gráfico", command=lambda: guardar_grafico(fig))
    btn_guardar.pack(pady=10)

# Función para guardar el gráfico
def guardar_grafico(fig):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Éxito", f"Gráfico guardado en {file_path}")

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de curvas florales")

# Agregar ícono de abeja
icon_path = "abejita.ico"  # Ruta correcta al ícono de abeja
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Estilo personalizado para la interfaz
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TCheckbutton", font=("Arial", 12))

# Crear widgets
ttk.Label(root, text="Nombre de la Planta:").grid(row=0, column=0, padx=10, pady=10)
planta_entry = ttk.Entry(root)
planta_entry.grid(row=0, column=1, padx=10, pady=10)

# Etiquetas para las quincenas en la parte superior
ttk.Label(root, text="1ra Quincena").grid(row=1, column=1, padx=10, pady=5)
ttk.Label(root, text="2da Quincena").grid(row=1, column=2, padx=10, pady=5)

# Crear los casilleros para las quincenas de cada mes
quincenas = []
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

for i, mes in enumerate(meses):
    ttk.Label(root, text=mes).grid(row=i+2, column=0, padx=10, pady=5, sticky="w")
    
    var_q1 = tk.IntVar()
    var_q2 = tk.IntVar()
    quincenas.append((var_q1, var_q2))
    
    ttk.Checkbutton(root, variable=var_q1).grid(row=i+2, column=1, padx=10, pady=5, ipadx=10, ipady=5)
    ttk.Checkbutton(root, variable=var_q2).grid(row=i+2, column=2, padx=10, pady=5, ipadx=10, ipady=5)

# Botón para agregar avistamiento
btn_agregar = ttk.Button(root, text="Agregar Avistamiento", command=agregar_avistamiento)
btn_agregar.grid(row=14, column=1, padx=10, pady=20)

# Lista para mostrar las plantas agregadas con los meses (sin repetición)
ttk.Label(root, text="Plantas Agregadas:").grid(row=15, column=0, padx=10, pady=10, sticky="w")
lista_plantas = tk.Listbox(root, height=5)
lista_plantas.grid(row=16, column=0, columnspan=3, padx=10, pady=5, sticky="we")

# Botón para mostrar el gráfico en una ventana nueva
btn_mostrar_grafico = ttk.Button(root, text="Mostrar Gráfico", command=mostrar_grafico)
btn_mostrar_grafico.grid(row=17, column=1, padx=10, pady=10)

root.mainloop()
