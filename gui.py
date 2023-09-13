import tkinter as tk
from tkinter import ttk, filedialog
import xml.etree.ElementTree as ET 

def Inicializar_clicked():
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, "Inicializando sistema.\n")

def Cargar_clicked():
    text_box.delete(1.0, tk.END)
    global archivo_abierto, loaded_xml_data

    archivo_abierto = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])  
    if archivo_abierto:
        try:
            tree = ET.parse(archivo_abierto)
            root_element = tree.getroot()
            loaded_xml_data = ET.tostring(root_element, encoding='utf-8').decode('utf-8')
            text_box.delete(1.0, tk.END)  
            text_box.insert(tk.END, loaded_xml_data)
        except Exception as e:
            text_box.delete(1.0, tk.END)  
            text_box.insert(tk.END, f"Error abriendo el  XML : {str(e)}\n")

def xmlSalida_clicked():
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, "Generando reporte de salida.\n")

def Ayuda_clicked():
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, "Natalia Mariel Calderon Echeverría\n")
    text_box.insert(tk.END, "202200007 - IPC 2 - SEGUNDO SEMESTRE 2023\n")
    text_box.insert(tk.END, "LINK: https://github.com/nxz7/IPC2_Proyecto2_202200007.git\n")
#archivo_abierto=None

def mensajes_opcion(event):
    global archivo_abierto, loaded_xml_data
    selected_item = combo_box.get()
    if selected_item == "Abrir":
        archivo_abierto = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if archivo_abierto:
            with open(archivo_abierto, 'r') as xml_file:
                loaded_xml_data = xml_file.read()
                text_box.delete(1.0, tk.END)  
                text_box.insert(tk.END, loaded_xml_data)

    elif selected_item == "Guardar":
        text_box.insert(tk.END, "No hay archivo abierto para guardar.\n")

    elif selected_item == "Guardar como":
        text_box.insert(tk.END, "No hay archivo abierto para guardar.\n")

    elif selected_item == "Salir":
        text_box.insert(tk.END, "No hay archivo abierto para guardar.\n")

def drones_opcion(event):
    selected_item = combo_box2.get()
    if selected_item == "listado":
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "listado.\n")

    elif selected_item == "agregar dron":
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "agregar dron.\n")
    elif selected_item == "Grafica sistema":
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Graficando sistema.\n")


root = tk.Tk()
root.title("PROYECTO 2- 202200007 - IPC2 - NCE")
root.configure(bg="lemon chiffon")


buttonAnalizar = tk.Button(root, text="Inicializar", command=Inicializar_clicked, bg="white", fg="blue")
buttonErrores = tk.Button(root, text="Cargar", command=Cargar_clicked, bg="white", fg="blue")
buttonReporte = tk.Button(root, text="Xml Salida", command=xmlSalida_clicked, bg="white", fg="blue")
buttonNuevo = tk.Button(root, text="Ayuda", command=Ayuda_clicked, bg="white", fg="blue")



combo_box = ttk.Combobox(root, values=["Listado de mensajes", "Guardar", "Guardar como", "Salir"])
combo_box.set("Gestion mensajes")
combo_box.bind("<<ComboboxSelected>>", mensajes_opcion)

combo_box2 = ttk.Combobox(root, values=["listado", "agregar dron","Grafica sistema"])
combo_box2.set("Gestion drones")
combo_box2.bind("<<ComboboxSelected>>", drones_opcion)


text_box = tk.Text(root)


buttonAnalizar.grid(row=0, column=0, padx=10, pady=10)
buttonErrores.grid(row=1, column=0, padx=10, pady=10)
buttonReporte.grid(row=2, column=0, padx=10, pady=10)
buttonNuevo.grid(row=3, column=0, padx=10, pady=10)
combo_box.grid(row=1, column=1, padx=10, pady=10)
combo_box2.grid(row=2, column=1, padx=10, pady=10)
text_box.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

root.mainloop()
