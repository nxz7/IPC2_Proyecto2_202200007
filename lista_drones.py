import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import simpledialog
from nodo_dron import nodo_dron

class lista_drones1:
    def __init__(self):
        self.cabeza= None

    def agregar_ordenados_a(self, data):
        nuevo_nodo = nodo_dron(data)

        if self.cabeza is None:
            self.cabeza= nuevo_nodo
            return

        if data < self.cabeza.data:
            nuevo_nodo.next = self.cabeza
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza
        while actual.next is not None and data > actual.next.data:
            actual = actual.next

        nuevo_nodo.next = actual.next
        actual.next = nuevo_nodo

    def mostrar_dron(self):
        actual = self.cabeza
        drones_text = ""
        while actual:
            drones_text += f"{actual.data}\n"
            actual = actual.next
        return drones_text


def llenar_dron_xml(xml_path):
    dron_lista = lista_drones1()

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for dron_e in root.find('.//listaDrones').iter('dron'):
        dron_nombre_A = dron_e.text
        dron_lista.agregar_ordenados_a(dron_nombre_A)

    return dron_lista

def agregar_actualizar_drones(xml_path, dron_lista):
    nuevo_dron_nombre = simpledialog.askstring("AGREGAR DRON", "Nombre del dron:")

    # VERIFICAR SI EXISTE
    if nuevo_dron_nombre is not None and nuevo_dron_nombre.strip() != "":
        actual = dron_lista.cabeza
        existe = False
        while actual:
            if actual.data == nuevo_dron_nombre:
                existe = True
                break
            actual = actual.next
        
        if not existe:
            # agregar el dron y actualizar la lista y que todavia este en orden alfabetico
            root = ET.parse(xml_path).getroot()
            lista_drones = root.find('.//listaDrones')
            nuevo_dron_e = ET.Element('dron')
            nuevo_dron_e.text = nuevo_dron_nombre
            lista_drones.append(nuevo_dron_e)
            tree = ET.ElementTree(root)
            tree.write(xml_path)
            
            dron_lista.agregar_ordenados_a(nuevo_dron_nombre)
            print(f"Dron: '{nuevo_dron_nombre}' agregado correctamente.")
        else:
            print(f"Dron: '{nuevo_dron_nombre}' ya existe.")
    else:
        print("NOMBRE NO VALIDO.")


