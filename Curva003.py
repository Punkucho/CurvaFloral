import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from random import randint
import numpy as np
from scipy.interpolate import make_interp_spline

# Datos iniciales
def inicializar_avistamientos():
    return {mes: [0, 0] for mes in range(12)}

avistamientos = inicializar_avistamientos()
colores = {}
plantas_avistadas = {}

def generar_color():
    return "#{:06x}".format(randint(0, 0xFFFFFF))

def agregar_avistamiento():
    planta = planta_entry.get()
    nombre_cientifico = nombre_cientifico_entry.get()
    if not planta:
        messagebox.showerror("Error", "Debe ingresar el nombre de la planta.")
        return
    
    if planta not in colores:
        colores[planta] = generar_color()
    
    meses_avistados = []
    for mes in range(12):
        if quincenas[mes][0].get() == 1 or quincenas[mes][1].get() == 1:
            if planta not in plantas_avistadas:
                plantas_avistadas[planta] = {"nombre_cientifico": nombre_cientifico, "meses": []}
            if mes not in plantas_avistadas[planta]["meses"]:
                plantas_avistadas[planta]["meses"].append(mes)
                meses_avistados.append(mes)
            if quincenas[mes][0].get() == 1:
                avistamientos[mes][0] += 1
            if quincenas[mes][1].get() == 1:
                avistamientos[mes][1] += 1

    if planta in plantas_avistadas:
        actualizar_lista_plantas()

    messagebox.showinfo("Éxito", f"Avistamiento de {planta} registrado.")
    planta_entry.delete(0, tk.END)
    nombre_cientifico_entry.delete(0, tk.END)
    for mes in range(12):
        quincenas[mes][0].set(0)
        quincenas[mes][1].set(0)

def actualizar_lista_plantas():
    lista_plantas.delete(0, tk.END)
    for planta, datos in plantas_avistadas.items():
        meses_texto = ", ".join(meses_nombres[mes] for mes in datos["meses"])
        lista_plantas.insert(tk.END, f"{planta} ({datos['nombre_cientifico']}) - Meses: {meses_texto}")
        lista_plantas.itemconfig(tk.END, {'fg': colores[planta]})

def mostrar_grafico():
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Crear o actualizar la figura y el canvas
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.set_title("Curva Floral Generada")
    ax.set_xlabel('Meses')
    ax.set_ylabel('Cantidad de Plantas')

    # Convertir las claves del diccionario a enteros
    avistamientos_int_keys = {int(k): v for k, v in avistamientos.items()}
    
    try:
        conteos = [sum(avistamientos_int_keys[mes]) for mes in range(12)]
    except KeyError as e:
        print(f"Error: Clave {e} no encontrada en avistamientos.")
        return

    # Ajustar datos para interpolar una curva suave
    x = np.arange(len(conteos))
    xnew = np.linspace(x.min(), x.max(), 300)
    spl = make_interp_spline(x, conteos, k=3)
    ynew = spl(xnew)
    
    # Crear etiquetas interpoladas para los meses
    meses_interpolados = np.linspace(0, 11, 300)
    ax.plot(meses_interpolados, ynew, label="Curva Promedio", color='blue')
    
    ax.set_xticks(np.arange(12))
    ax.set_xticklabels(meses)
    
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=7, rowspan=17, padx=10, pady=10, sticky='nsew')

def guardar_grafico(fig):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        fig.savefig(file_path)
        messagebox.showinfo("Éxito", f"Gráfico guardado en {file_path}")

def guardar_datos():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        datos = {
            "avistamientos": avistamientos,
            "colores": colores,
            "plantas_avistadas": plantas_avistadas
        }
        with open(file_path, "w") as f:
            json.dump(datos, f)
        messagebox.showinfo("Éxito", f"Datos guardados en {file_path}")

def cargar_datos():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as f:
            datos = json.load(f)
            global avistamientos, colores, plantas_avistadas
            avistamientos = {int(k): v for k, v in datos["avistamientos"].items()}
            colores = datos["colores"]
            plantas_avistadas = datos["plantas_avistadas"]
        actualizar_lista_plantas()
        messagebox.showinfo("Éxito", "Datos cargados exitosamente")

def eliminar_planta():
    seleccionado = lista_plantas.curselection()
    if seleccionado:
        texto_seleccionado = lista_plantas.get(seleccionado[0])
        planta = texto_seleccionado.split(" - ")[0].split(" (")[0]
        if planta in plantas_avistadas:
            # Eliminar la planta de avistamientos
            for mes in plantas_avistadas[planta]["meses"]:
                avistamientos[mes][0] -= 1
                avistamientos[mes][1] -= 1
            del plantas_avistadas[planta]
            del colores[planta]
            actualizar_lista_plantas()
            messagebox.showinfo("Éxito", f"Planta {planta} eliminada.")

def editar_planta():
    seleccionado = lista_plantas.curselection()
    if seleccionado:
        planta = lista_plantas.get(seleccionado[0]).split(" - ")[0].split(" (")[0]
        if planta in plantas_avistadas:
            datos = plantas_avistadas[planta]
            planta_entry.delete(0, tk.END)
            planta_entry.insert(0, planta)
            nombre_cientifico_entry.delete(0, tk.END)
            nombre_cientifico_entry.insert(0, datos["nombre_cientifico"])
            for mes in range(12):
                quincenas[mes][0].set(1 if mes in datos["meses"] else 0)
                quincenas[mes][1].set(1 if mes in datos["meses"] else 0)

def crear_barra_menu():
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    menu_archivo = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
    menu_archivo.add_command(label="Guardar Datos", command=guardar_datos)
    menu_archivo.add_command(label="Cargar Datos", command=cargar_datos)
    menu_archivo.add_command(label="Salir", command=root.quit)

    menu_editar = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Editar", menu=menu_editar)
    menu_editar.add_command(label="Editar Planta", command=editar_planta)

def on_click_lista(event):
    menu_contextual.post(event.x_root, event.y_root)

root = tk.Tk()
root.title("Generador de curvas florales")

# Asignar el ícono a la ventana principal
root.iconbitmap('abejita.ico')

# Crear barra de menú
crear_barra_menu()

# Campos de entrada
ttk.Label(root, text="Nombre de la Planta:").grid(row=0, column=0, padx=10, pady=10)
planta_entry = ttk.Entry(root)
planta_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

ttk.Label(root, text="Nombre Científico (opcional):").grid(row=1, column=0, padx=10, pady=10)
nombre_cientifico_entry = ttk.Entry(root)
nombre_cientifico_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

ttk.Button(root, text="Agregar Avistamiento", command=agregar_avistamiento).grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Selección de meses y quincenas
meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
quincenas = []
for mes in range(12):
    ttk.Label(root, text=meses_nombres[mes]).grid(row=3+mes, column=0, padx=10, pady=10)
    q1 = tk.IntVar()
    q2 = tk.IntVar()
    quincenas.append([q1, q2])
    ttk.Checkbutton(root, text="Quincena 1", variable=q1).grid(row=3+mes, column=1, padx=10, pady=10)
    ttk.Checkbutton(root, text="Quincena 2", variable=q2).grid(row=3+mes, column=2, padx=10, pady=10)

# Listbox para mostrar plantas agregadas
lista_plantas = tk.Listbox(root)
lista_plantas.grid(row=0, column=4, rowspan=17, padx=10, pady=10, sticky='nsew')
lista_plantas.bind("<Button-3>", on_click_lista)

# Menú contextual
menu_contextual = tk.Menu(root, tearoff=0)
menu_contextual.add_command(label="Eliminar Planta", command=eliminar_planta)

# Botones para mostrar y guardar gráfico
ttk.Button(root, text="Generar Gráfico", command=mostrar_grafico).grid(row=18, column=0, columnspan=2, padx=10, pady=10)
ttk.Button(root, text="Guardar Gráfico", command=lambda: guardar_grafico(None)).grid(row=18, column=2, columnspan=2, padx=10, pady=10)

root.mainloop()
