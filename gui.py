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
    lista_sistemas_drones.clear_lista()
    dron_lista.clear_listaDrones()
    lista_mensajes_llena.clear_listaMensaje()
    lista_significados_concatenados.clear_listaFinal()
    text_box.insert(tk.END, "*****SISTEMA INICIALIZADO******.\n")


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
    text_box.insert(tk.END, "Generating reporte de salida.\n")

    if lista_significados_concatenados is not None:
        
        root = ET.Element("respuesta")
        listaMensajes = ET.SubElement(root, "listaMensajes")

        for mensaje_item in lista_significados_concatenados.iter_nodes():
            
            sistema_actual = lista_sistemas_drones.cabecera
            altura_maxima = None  

            while sistema_actual:
                if sistema_actual.nombre == mensaje_item.sis_nombre:
                    altura_maxima = sistema_actual.altura_maxima
                    break  # para cuando encuentra el sistema

                sistema_actual = sistema_actual.siguiente

            if altura_maxima is not None:
                mensaje = ET.SubElement(listaMensajes, "mensaje", nombre=mensaje_item.mens_nombre)
                sistemaDrones = ET.SubElement(mensaje, "sistemaDrones")
                sistemaDrones.text = mensaje_item.sis_nombre

                Altura = ET.SubElement(mensaje, "tiempoOptimo")
                Altura.text = str(altura_maxima)

                mensajeRecibido = ET.SubElement(mensaje, "mensajeRecibido")
                mensajeRecibido.text = mensaje_item.conc_significado

                # busca el sistema que se esta viendo
                sistema_actual = lista_sistemas_drones.cabecera
                while sistema_actual:
                    if sistema_actual.nombre == mensaje_item.sis_nombre:
                        instrucciones = ET.SubElement(mensaje, "instrucciones")

                        for altura in range(1, altura_maxima + 1):
                            altura_element = ET.SubElement(instrucciones, "tiempo", valor=str(altura))
                            acciones = ET.SubElement(altura_element, "acciones")

                            dron_actual = sistema_actual.cabecera_drones
                            while dron_actual:
                                altura_actual = dron_actual.cabecera_alturas
                                while altura_actual and altura_actual.valor != altura:
                                    altura_actual = altura_actual.siguiente
                                if altura_actual:
                                    dron_element = ET.SubElement(acciones, "dron", nombre=dron_actual.nombre_dron)
                                    dron_element.text = altura_actual.datos  
                                else:
                                    dron_element = ET.SubElement(acciones, "dron", nombre=dron_actual.nombre_dron)
                                    dron_element.text = ""  # si no existe/no encuentra 
                                dron_actual = dron_actual.siguiente

                    sistema_actual = sistema_actual.siguiente

        
        tree = ET.ElementTree(root)
        tree.write("salida.xml", encoding="UTF-8", xml_declaration=True, method="xml", short_empty_elements=False)
        
        # la identacion u los espacion
        import xml.dom.minidom
        xml = xml.dom.minidom.parse("salida.xml")
        with open("salida.xml", "w") as xml_file:
            xml_file.write(xml.toprettyxml())

        text_box.insert(tk.END, "Reporte de salida GENERADO salida.xml.\n")
    else:
        text_box.insert(tk.END, "NO HAY INFORMACION SOBRE EL RECORRIDO.\n")

def Ayuda_clicked():
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, "Natalia Mariel Calderon Echeverría\n")
    text_box.insert(tk.END, "202200007 - IPC 2 - SEGUNDO SEMESTRE 2023\n")
    text_box.insert(tk.END, "LINK: https://github.com/nxz7/IPC2_Proyecto2_202200007.git\n")

archivo_abierto=None
#------------------------------------------
lista_mensajes_llena = None  


            
# !!!!!!!!!!!!!! significado de los mensajes --------> xml de salida
class nodo_final:
    def __init__(self, sis_nombre, mens_nombre, conc_significado):
        self.sis_nombre = sis_nombre
        self.mens_nombre = mens_nombre
        self.conc_significado = conc_significado
        self.next = None

class lista_final:
    def __init__(self):
        self.head = None

    def append(self, sis_nombre, mens_nombre, conc_significado):
        new_node = nodo_final(sis_nombre, mens_nombre, conc_significado)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def iter_nodes(self):
        current = self.head
        while current:
            yield current
            current = current.next
    def clear_listaFinal(self):
        self.head = None


lista_significados_concatenados=None
lista_significados_concatenados = lista_final()

def llenar_lista_significados_concatenados(lista_mensajes, lista_sistemas_drones):
    global lista_mensajes_llena,lista_significados_concatenados

    root = tk.Tk()
    root.withdraw()
    nombre_mensaje = askstring("Input", "INGRESE NOMBRE DEL MENSAJE:")

    if nombre_mensaje is not None:
        if lista_mensajes_llena is None:
            lista_mensajes_llena = parse_mensaje(archivo_abierto)

        #lista_significados_concatenados = lista_final()  

        sis_nombre = None
        mens_nombre = None
        conc_significado = ""

        actual = lista_mensajes.cabeza
        while actual:
            if actual.nombre_mensaje == nombre_mensaje:
                significado = buscar_sistema_dron_altura(
                    lista_sistemas_drones,
                    actual.nombre_sistema,
                    actual.dron,
                    int(actual.valor)
                )
                actual.significado = significado
                
                if sis_nombre is None and mens_nombre is None:
                    sis_nombre = actual.nombre_sistema
                    mens_nombre = actual.nombre_mensaje
                
                if actual.nombre_sistema == sis_nombre and actual.nombre_mensaje == mens_nombre:
                    conc_significado += actual.significado
                
            actual = actual.next


        lista_significados_concatenados.append(sis_nombre, mens_nombre, conc_significado)


        #text_box.delete(1.0, tk.END)
        current = lista_significados_concatenados.head
        while current:
            text_box.insert(tk.END, f"nombre_sistema: {current.sis_nombre}, nombre_mensaje: {current.mens_nombre}, significado: {current.conc_significado}\n")
            current = current.next

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
        #text_box.delete(1.0, tk.END) 
        text_box.insert(tk.END, "Seleccionar mensaje.\n")
        #mostrar_mensaje_significado(lista_mensajes_llena,lista_sistemas_drones)
        llenar_lista_significados_concatenados(lista_mensajes_llena, lista_sistemas_drones)

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
        #text_box.delete(1.0, tk.END)
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
