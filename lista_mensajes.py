import xml.etree.ElementTree as ET
from nodo_mensaje import nodo_mensaje

class lista_mensajes:
    def __init__(self):
        self.cabeza = None

    def append(self, nodo):
        if not self.cabeza:
            self.cabeza = nodo
        else:
            actual = self.cabeza
            while actual.next:
                actual = actual.next
            actual.next = nodo

def parse_mensaje(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    lista_mensajesC = lista_mensajes()

    for mensaje in root.findall(".//Mensaje"):
        sistema_drones = mensaje.find("sistemaDrones").text
        instrucciones = mensaje.find(".//instrucciones")
        for instruccion in instrucciones.findall("instruccion"):
            dron = instruccion.get("dron")
            valor = instruccion.text
            mensaje_nombre = mensaje.get('nombre')

            nodo = nodo_mensaje(sistema_drones, mensaje_nombre, dron, valor,significado=None)
            lista_mensajesC.append(nodo)

    return lista_mensajesC

def imprimir_mensajes(lista_mensajesC):
    actual = lista_mensajesC.cabeza
    mensaje_text = ""

    while actual:
        comun_nombre_sistema = actual.nombre_sistema
        comun_nombre_mensaje = actual.nombre_mensaje

        mensaje_text += f"{comun_nombre_sistema}, {comun_nombre_mensaje}\n"

        while actual and actual.nombre_sistema == comun_nombre_sistema and actual.nombre_mensaje == comun_nombre_mensaje:
            mensaje_text += f"  {actual.dron}, {actual.valor}\n"
            actual = actual.next

        mensaje_text += "\n"

    return mensaje_text


