import tkinter as tk
from tkinter import colorchooser
import subprocess
import webbrowser
import json
from PIL import Image, ImageTk

# Función para ejecutar la tarea asignada
def ejecutar_tarea(comando):
    if comando.startswith("http"):
        webbrowser.open(comando)
    else:
        subprocess.run(comando, shell=True)

# Función para abrir el menú de configuración del botón
def configurar_boton(boton_id):
    color = configuraciones[boton_id]["color"]  # Obtener el color actual

    def guardar_configuracion():
        # Guardar color y comando
        configuraciones[boton_id]["color"] = color
        configuraciones[boton_id]["comando"] = entry_comando.get()
        
        # Aplicar color al botón
        botones[boton_id].config(bg=color)
        guardar_configuraciones()
        ventana_configuracion.destroy()

    # Selección de color
    def seleccionar_color():
        nonlocal color  # Usamos nonlocal aquí para referirnos a la variable 'color'
        color = colorchooser.askcolor()[1]
        btn_color.config(bg=color)

    # Crear ventana de configuración
    ventana_configuracion = tk.Toplevel()
    ventana_configuracion.title(f"Configurar botón {boton_id}")
    
    # Mantener ventana en primer plano hasta que se cierre
    ventana_configuracion.grab_set()

    tk.Label(ventana_configuracion, text="Comando (ruta, URL, o programa):").pack(pady=5)
    entry_comando = tk.Entry(ventana_configuracion)
    entry_comando.pack(pady=5)
    entry_comando.insert(0, configuraciones[boton_id]["comando"])  # Prellenar con el comando actual

    tk.Label(ventana_configuracion, text="Color del botón:").pack(pady=5)
    btn_color = tk.Button(ventana_configuracion, text="Seleccionar color", command=seleccionar_color, bg=color)
    btn_color.pack(pady=5)

    tk.Button(ventana_configuracion, text="Guardar", command=guardar_configuracion).pack(pady=5)

# Guardar configuraciones en archivo JSON
def guardar_configuraciones():
    with open("configuraciones.json", "w") as archivo:
        json.dump(configuraciones, archivo)

# Cargar configuraciones desde archivo JSON
def cargar_configuraciones():
    try:
        with open("configuraciones.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Touch Portal Configurable")
ventana.geometry("500x300")

# Diccionario para almacenar configuraciones de botones
configuraciones = cargar_configuraciones()

# Crear 4 botones y sus configuraciones
botones = {}
imagenes = {}

# Rutas fijas de imágenes
rutas_imagenes = [
    "depositphotos_3417684.jpg",
    "png-clipart-button-drawing-lighter-pushbutton-red-button.png",
    "png-clipart-product-blue-circle-font-button-miscellaneous-blue.png",
    "botón-amarillo-126381219.webp"
]

# Crear 4 botones
for i in range(4):
    # Cargar configuraciones previas
    if i in configuraciones:
        color = configuraciones[i].get("color", "gray")
        comando = configuraciones[i].get("comando", "")
    else:
        color = "gray"
        comando = ""
    
    # Cargar imagen fija
    try:
        img = Image.open(rutas_imagenes[i])
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        botones[i] = tk.Button(ventana, bg=color, image=img_tk, command=lambda c=comando: ejecutar_tarea(c))
        botones[i].image = img_tk  # Guardar referencia a la imagen
    except Exception as e:
        print(f"Error al cargar la imagen {rutas_imagenes[i]}: {e}")
        botones[i] = tk.Button(ventana, bg=color, text=f"Botón {i+1}", width=10, height=5, command=lambda c=comando: ejecutar_tarea(c))

    botones[i].grid(row=0, column=i, padx=10, pady=10)
    
    boton_configurar = tk.Button(ventana, text="Configurar", command=lambda i=i: configurar_boton(i))
    boton_configurar.grid(row=1, column=i, padx=10, pady=10)

ventana.mainloop()
