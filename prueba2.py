import tkinter as tk
import subprocess
import webbrowser
import json
from PIL import Image, ImageTk

# Función para ejecutar la tarea asignada
def ejecutar_tarea(comando):
    if comando.startswith("http"):
        webbrowser.open(comando)
    else:
        try:
            subprocess.run(comando, shell=True)
        except Exception as e:
            print(f"Error al ejecutar la tarea: {e}")

# Función para abrir el menú de configuración del botón
def configurar_boton(boton_id):
    nombre_boton = configuraciones[boton_id].get("nombre", f"Botón {boton_id + 1}")  # Nombre actual
    comando_actual = configuraciones[boton_id]["comando"]

    def guardar_configuracion():
        # Guardar comando y nombre
        configuraciones[boton_id]["comando"] = entry_comando.get()
        configuraciones[boton_id]["nombre"] = entry_nombre.get()

        # Aplicar nombre al botón
        botones[boton_id].config(text=entry_nombre.get())
        boton_configurar[boton_id].config(text=entry_nombre.get())  # Actualizar texto del botón de configuración
        guardar_configuraciones()
        ventana_configuracion.destroy()

    def eliminar_comando():
        # Eliminar comando
        configuraciones[boton_id]["comando"] = ""
        entry_comando.delete(0, tk.END)  # Limpiar entrada de comando
        eliminar_button.config(state=tk.DISABLED)  # Desactivar el botón de eliminar

    # Crear ventana de configuración
    ventana_configuracion = tk.Toplevel()
    ventana_configuracion.title(f"Configurar botón {boton_id}")

    # Mantener ventana en primer plano hasta que se cierre
    ventana_configuracion.grab_set()

    tk.Label(ventana_configuracion, text="Comando (ruta, URL, o programa):").pack(pady=5)
    entry_comando = tk.Entry(ventana_configuracion, width=40)
    entry_comando.pack(pady=5)
    entry_comando.insert(0, comando_actual)  # Prellenar con el comando actual

    tk.Label(ventana_configuracion, text="Nombre del botón:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_configuracion)
    entry_nombre.pack(pady=5)
    entry_nombre.insert(0, nombre_boton)  # Prellenar con el nombre actual

    # Botón para eliminar comando
    eliminar_button = tk.Button(ventana_configuracion, text="Eliminar comando", command=eliminar_comando)
    eliminar_button.pack(pady=5)

    if comando_actual:  # Si hay un comando ya configurado, habilitar el botón de eliminar
        eliminar_button.config(state=tk.NORMAL)
    else:
        eliminar_button.config(state=tk.DISABLED)

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

# Si no hay configuraciones, inicializarlas
for i in range(4):
    if i not in configuraciones:
        configuraciones[i] = {
            "comando": "",
            "nombre": f"Botón {i + 1}"
        }

# Crear 4 botones y sus configuraciones
botones = {}
boton_configurar = {}

# Rutas fijas de imágenes
rutas_imagenes = [
    "png-transparent-colorful-arcade-button-set.jpg",
    "png-transparent-colorful-arcade-button-set2.jpg",
    "png-transparent-colorful-arcade-button-set3.jpg",
    "png-transparent-colorful-arcade-button-set4.jpg"
]

# Crear 4 botones
for i in range(4):
    # Cargar configuraciones previas
    comando = configuraciones[i].get("comando", "")
    nombre_boton = configuraciones[i].get("nombre", f"Botón {i + 1}")

    # Cargar imagen fija
    try:
        img = Image.open(rutas_imagenes[i])
        img = img.resize((100, 100), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        botones[i] = tk.Button(ventana, image=img_tk, text=nombre_boton, command=lambda c=comando: ejecutar_tarea(c))
        botones[i].image = img_tk  # Guardar referencia a la imagen
    except Exception as e:
        print(f"Error al cargar la imagen {rutas_imagenes[i]}: {e}")
        botones[i] = tk.Button(ventana, text=nombre_boton, width=10, height=5, command=lambda c=comando: ejecutar_tarea(c))

    botones[i].grid(row=0, column=i, padx=10, pady=10)

    boton_configurar[i] = tk.Button(ventana, text="Configurar", command=lambda i=i: configurar_boton(i))
    boton_configurar[i].grid(row=1, column=i, padx=10, pady=10)

ventana.mainloop()

