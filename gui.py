import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.simpledialog import askstring
import xml.etree.ElementTree as ET 
from lista_sistema import NodoSistema, imprimir_tabla, ListaSistemasDrones, parse_xml, generar_archivo_sistema,escribir_dot_sistema,buscar_sistema_dron_altura
from lista_drones import lista_drones1, llenar_dron_xml,agregar_actualizar_drones
from lista_mensajes import imprimir_mensajes, lista_mensajes,parse_mensaje

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
#------------------------------------------
lista_mensajes_llena = None  


#----------------------LISTA RAPIDA PARA IR MOSTRANDO LOS MENSAJE-----------------------
class NodoMensajeSignificado:
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.next = None

class ListaMensajeSignificado:
    def __init__(self):
        self.cabeza = None

    def append(self, mensaje):
        nuevo_nodo = NodoMensajeSignificado(mensaje)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            current = self.cabeza
            while current.next:
                current = current.next
            current.next = nuevo_nodo
#----------------------LISTA RAPIDA PARA IR MOSTRANDO LOS MENSAJE-----------------------


def mostrar_mensaje_significado(lista_mensajes, lista_sistemas_drones):
    global lista_mensajes_llena  

    root = tk.Tk()
    root.withdraw()  
    nombre_mensaje = askstring("Input", "INGRESE NOMBRE DEL MENSAJE:")

    if nombre_mensaje is not None:  
        if lista_mensajes_llena is None:
            lista_mensajes_llena = parse_mensaje(archivo_abierto)

        actual = lista_mensajes.cabeza
        mensaje_significado_lista = ListaMensajeSignificado()  # LA LISTA RAPIDA DE ARRIBA PARA IR GUARDANDO LAS LETRAS DEL SIGNiFOCADO
        while actual:
            if actual.nombre_mensaje == nombre_mensaje:
                # BUSCAR EL SIGNIFICADO QUE ES LA LETRA
                significado = buscar_sistema_dron_altura(
                    lista_sistemas_drones,
                    actual.nombre_sistema,
                    actual.dron,
                    int(actual.valor)
                )
                actual.significado = significado
                mensaje_significado_lista.append(
                    f"nombre_sistema: {actual.nombre_sistema}, "
                    f"nombre_mensaje: {actual.nombre_mensaje}, "
                    f"significado: {actual.significado}"
                )
            actual = actual.next

        # PONERLO EN TEXTBOX
        text_box.delete(1.0, tk.END)
        current = mensaje_significado_lista.cabeza
        while current:
            text_box.insert(tk.END, current.mensaje + "\n")
            current = current.next


#------------------------------------------MENSAJES/RECORRIDO/SUBIR/BAJAR/ESPERAR

def mostrar_mensaje_mod(lista_mensajes, lista_sistemas_drones):
    global lista_mensajes_llena  

    root = tk.Tk()
    root.withdraw()  

    if lista_mensajes_llena is None:
        lista_mensajes_llena = parse_mensaje(archivo_abierto)

    actual = lista_mensajes.cabeza
    while actual:
        # EMITIR LUZ
        recorrido_sistema_dron_altura(
            lista_sistemas_drones,
            actual.nombre_sistema,
            actual.dron,
            int(actual.valor),
            "emitir luz"
        )

        actual = actual.next

    # SUBIR/ESPERAR/BAJAR
    verificar_sistema_dron_altura(lista_sistemas_drones)

    # VERIFICAR/ IMPRIMIR
    #imprimir_lista_sistemas_mod(lista_sistemas_drones)

def verificar_sistema_dron_altura(lista_sistemas_drones):
    sistema_actual = lista_sistemas_drones.cabecera
    while sistema_actual:
        dron_actual = sistema_actual.cabecera_drones
        emitir_luz_altura = None  # LLEVAR EL QUE YA TIENE EMITIR LUZ
        while dron_actual:
            altura_actual = dron_actual.cabecera_alturas
            prev_altura_actual = None  # PARA VER LA ALTURA SI VA SUBIENDO O BAJANDO
            while altura_actual:
                if altura_actual.datos == "emitir luz":
                    emitir_luz_altura = altura_actual.valor  # EMITIR LUZ
                elif emitir_luz_altura is not None:
                    # SUBIR/ESPERAR
                    if altura_actual.valor < emitir_luz_altura:
                        altura_actual.datos = "subir"
                    else:
                        altura_actual.datos = "esperar"
                prev_altura_actual = altura_actual
                altura_actual = altura_actual.siguiente
            dron_actual = dron_actual.siguiente
        sistema_actual = sistema_actual.siguiente



def recorrido_sistema_dron_altura(lista_sistemas_drones, nombre_sistema, nombre_dron, valor_altura, n_significado):
    sistema_actual = lista_sistemas_drones.cabecera
    while sistema_actual:
        if sistema_actual.nombre == nombre_sistema:
            dron_actual = sistema_actual.cabecera_drones
            while dron_actual:
                if dron_actual.nombre_dron == nombre_dron:
                    altura_actual = dron_actual.cabecera_alturas
                    while altura_actual:
                        if altura_actual.valor == valor_altura:
                            altura_actual.datos = n_significado
                            return
                        altura_actual = altura_actual.siguiente
                dron_actual = dron_actual.siguiente
        sistema_actual = sistema_actual.siguiente

def imprimir_lista_sistemas_mod(lista_sistemas_drones):
    result = ""  
    sistema_actual = lista_sistemas_drones.cabecera
    while sistema_actual:
        result += f"*************************************************\n"
        result += f"Sistema: {sistema_actual.nombre}_RECORRIDO\n"
        result += f"tiempo: {sistema_actual.altura_maxima} segundos\n"

        dron_actual = sistema_actual.cabecera_drones
        fila_encabezado = "\t"
        while dron_actual:
            fila_encabezado += f"{dron_actual.nombre_dron}      \t"
            dron_actual = dron_actual.siguiente
        result += fila_encabezado + "\n"

        for altura in range(1, sistema_actual.altura_maxima + 1):
            fila_datos = f"{altura}\t"
            dron_actual = sistema_actual.cabecera_drones
            while dron_actual:
                altura_actual = dron_actual.cabecera_alturas
                while altura_actual and altura_actual.valor != altura:
                    altura_actual = altura_actual.siguiente
                if altura_actual:
                    fila_datos += f"{altura_actual.datos}    \t"
                else:
                    fila_datos += "\t"
                dron_actual = dron_actual.siguiente
            result += fila_datos + "\n"

        sistema_actual = sistema_actual.siguiente
    return result  # el formato para que vaya en el textbox

def mostrar_imprimir_tabla_recorrido():
    global lista_sistemas_drones
    text_box.delete(1.0, tk.END)
    try:
        text = "***************************Sistema/mensaje******************************\n"
        text += "********************recorrido - tiempo optimo**************************\n"
        text += imprimir_lista_sistemas_mod(lista_sistemas_drones)
        return text  
    except Exception as e:
        text_box.insert(tk.END, f"error en el xml: {str(e)}\n")
        return ""

#-------------------------------------------------
def mensajes_opcion(event):
    global archivo_abierto, loaded_xml_data,lista_mensajes_llena 
    selected_item = combo_box.get()
    #listado ------------------------------------
    if selected_item == "Listado de mensajes":
        text_box.insert(tk.END, "Listado de mensajes:.\n")
        lista_mensajes_llena = parse_mensaje(archivo_abierto)
        mensaje_text = imprimir_mensajes(lista_mensajes_llena)
        text_box.delete(1.0, tk.END)  
        text_box.insert(tk.END, mensaje_text)
    #elegir mensaje y lo del tiempo ------------------------------------
    elif selected_item == "seleccionar mensaje":
        text_box.insert(tk.END, "Seleccionar mensaje.\n")
        mostrar_mensaje_significado(lista_mensajes_llena,lista_sistemas_drones)

    elif selected_item == "modificar":
        text_box.insert(tk.END, "modificar.\n")
        mostrar_mensaje_mod(lista_mensajes_llena, lista_sistemas_drones)
        text = mostrar_imprimir_tabla_recorrido()
        text_box.insert(tk.END, text)
        output_folder = 'C:/Users/natalia/Documents/4sem/ipc2/lab/IPC2_Proyecto2_202200007'
        
        # LOS NOMBRE DE LOS ARCHIVOS QUE VAN A SER LOS DEL SISTEMA SIN EXTENSION
        dot_nombres = lista_nombre_ar()

        #  - HACER EL DOT
        sistema_actual = lista_sistemas_drones.cabecera
        while sistema_actual:
            dot_codigo_es = escribir_dot_sistema(sistema_actual)
            dot_nombreAR = f'{sistema_actual.nombre}_instrucciones.dot'
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


    elif selected_item == "Salir":
        text_box.insert(tk.END, "salir.\n")

lista_sistemas_drones=None
#-------------------
def mostrar_imprimir_tabla():
    global lista_sistemas_drones
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



combo_box = ttk.Combobox(root, values=["Listado de mensajes", "seleccionar mensaje", "modificar", "Salir"])
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
