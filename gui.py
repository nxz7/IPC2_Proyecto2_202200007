import os
import tkinter as tk
from tkinter import ttk, filedialog
import xml.etree.ElementTree as ET 
from lista_sistema import imprimir_tabla, ListaSistemasDrones, parse_xml, generar_archivo_sistema,escribir_dot_sistema
from lista_drones import lista_drones1, llenar_dron_xml,agregar_actualizar_drones


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
            lista_sistemas_drones = parse_xml(archivo_abierto)
            text_box.insert(tk.END, "*********************** CREANDO SISTEMAS **************************\n")
            text_box.insert(tk.END, "****************CONTENIDO ANALIZADO - SISTEMAS CREADOS************\n")
            #imprimir_tabla(lista_sistemas_drones)
            #text_box.insert(tk.END, tabla)
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

archivo_abierto=None

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


def mostrar_imprimir_tabla():
    text_box.delete(1.0, tk.END)
    try:
        lista_sistemas_drones = parse_xml(archivo_abierto)
        text = "**************************************************************\n"
        text += "********************Sistemas Drones **************************\n"
        text += imprimir_tabla(lista_sistemas_drones)
        return text  
    except Exception as e:
        text_box.insert(tk.END, f"error en el xml: {str(e)}\n")
        return ""  

def mostrar_lista_drones():
    global archivo_abierto
    text_box.delete(1.0, tk.END)
    try:
        dron_lista = llenar_dron_xml(archivo_abierto)
        drones_text = dron_lista.mostrar_dron()  # agarrar la string del dron
        text_box.insert(tk.END, "Listado de Drones:\n")
        text_box.insert(tk.END, drones_text)  
    except Exception as e:
        text_box.insert(tk.END, f"Error en el XML: {str(e)}\n")


#----------------------------------------------------------
#lista rapida que lleva el control de los nombres de los archivos
class nodo_nombre_ar:
    def __init__(self, value):
        self.value = value
        self.next = None

class lista_nombre_ar:
    def __init__(self):
        self.cabeza = None

    def append(self, value):
        nuevo_nn = nodo_nombre_ar(value)
        if not self.cabeza:
            self.cabeza = nuevo_nn
        else:
            current = self.cabeza
            while current.next:
                current = current.next
            current.next = nuevo_nn
#---------------------------------------------------

def drones_opcion(event):
    selected_item = combo_box2.get()
    global dron_lista
    if selected_item == "listado":
        text_box.delete(1.0, tk.END)
        dron_lista = llenar_dron_xml(archivo_abierto)
        dron_lista.mostrar_dron()
        text_box.insert(tk.END, "Listado de drones\n")
        mostrar_lista_drones()
    elif selected_item == "agregar dron":
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "agregar dron.\n")
        agregar_actualizar_drones(archivo_abierto, dron_lista)
        text_box.insert(tk.END, "dron agregado.\n")
    elif selected_item == "Grafica sistema":
        text_box.delete(1.0, tk.END)
        text = mostrar_imprimir_tabla()
        text_box.insert(tk.END, text)
        lista_sistemas_drones = parse_xml(archivo_abierto)
        output_folder = 'C:/Users/natalia/Documents/4sem/ipc2/lab/IPC2_Proyecto2_202200007'
        
        # LOS NOMBRE DE LOS ARCHIVOS QUE VAN A SER LOS DEL SISTEMA SIN EXTENSION
        dot_nombres = lista_nombre_ar()

        #  - HACER EL DOT
        sistema_actual = lista_sistemas_drones.cabecera
        while sistema_actual:
            dot_codigo_es = escribir_dot_sistema(sistema_actual)
            dot_nombreAR = f'{sistema_actual.nombre}.dot'
            dot_file_path = os.path.join(output_folder, dot_nombreAR)
            with open(dot_file_path, 'w') as dot_file:
                dot_file.write(dot_codigo_es)
            dot_nombres.append(dot_nombreAR)
            sistema_actual = sistema_actual.siguiente

        # HACER EL PNG
        current_nodo = dot_nombres.cabeza
        while current_nodo:
            dot_nombreAR = current_nodo.value
            png_nombreAR = dot_nombreAR.replace(".dot", ".png")
            dot_ar_path = os.path.join(output_folder, dot_nombreAR)
            png_ar_path = os.path.join(output_folder, png_nombreAR)
            os.system(f'dot -Tpng "{dot_ar_path}" -o "{png_ar_path}"')
            current_nodo = current_nodo.next

        text_box.insert(tk.END, "***** GRAFICOS GENERADOS SATISFACTORIAMENTE *****\n")



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
