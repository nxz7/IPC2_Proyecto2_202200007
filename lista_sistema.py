import xml.etree.ElementTree as ET
import os

class NodoAltura:
    def __init__(self, valor, datos):
        self.valor = valor
        self.datos = datos
        self.siguiente = None
        self.anterior = None

class NodoDron:
    def __init__(self, nombre_dron):
        self.nombre_dron = nombre_dron
        self.siguiente = None
        self.anterior = None
        self.cabecera_alturas = None  # INICIO DE LA LISTA DE ALTURAS

class NodoSistema:
    def __init__(self, nombre, altura_maxima, cantidad_drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.siguiente = None
        self.anterior = None
        self.cabecera_drones = None  # INICIO LISTA DE DRONES QUE ES OTRA LISTA

class ListaSistemasDrones:
    def __init__(self):
        self.cabecera = None
        self.cola = None

    def agregar(self, nodo_sistema):
        if self.cola is None:
            self.cabecera = nodo_sistema
            self.cola = nodo_sistema
        else:
            self.cola.siguiente = nodo_sistema
            nodo_sistema.anterior = self.cola
            self.cola = nodo_sistema

def parse_xml(ruta_archivo_xml):
    # INSTANCIA DE LA LISTA BASE DE DRONES PARA LLENAR LISTAS
    lista_sistemas_drones = ListaSistemasDrones()

    # LEER Y PARSEAR EL XML
    arbol = ET.parse(ruta_archivo_xml)
    raiz = arbol.getroot()
    elemento_lista_sistemas_drones = raiz.find('listaSistemasDrones')

    # Iterar en los elementos de sistema de drones
    for elemento_sistema in elemento_lista_sistemas_drones.findall('sistemaDrones'):
        nombre = elemento_sistema.get('nombre')
        altura_maxima = int(elemento_sistema.find('alturaMaxima').text)
        cantidad_drones = int(elemento_sistema.find('cantidadDrones').text)

        nodo_sistema = NodoSistema(nombre, altura_maxima, cantidad_drones)

        # Iterar en el contenido - LETRAS
        for elemento_contenido in elemento_sistema.findall('contenido'):
            nombre_dron = elemento_contenido.find('dron').text
            nodo_dron = NodoDron(nombre_dron)

            # Alturas
            for elemento_altura in elemento_contenido.find('alturas'):
                valor = int(elemento_altura.get('valor'))
                datos = elemento_altura.text
                nodo_altura = NodoAltura(valor, datos)

                # Unir el nodo de altura con el del dron para formar la lista doble ------- Paso 1 de la lista de listas
                if nodo_dron.cabecera_alturas is None:
                    nodo_dron.cabecera_alturas = nodo_altura
                else:
                    altura_actual = nodo_dron.cabecera_alturas
                    while altura_actual.siguiente is not None:
                        altura_actual = altura_actual.siguiente
                    altura_actual.siguiente = nodo_altura
                    nodo_altura.anterior = altura_actual

            # Ahora unir el dron a la lista de drones ------- Paso 2 de la lista de listas
            if nodo_sistema.cabecera_drones is None:
                nodo_sistema.cabecera_drones = nodo_dron
            else:
                dron_actual = nodo_sistema.cabecera_drones
                while dron_actual.siguiente is not None:
                    dron_actual = dron_actual.siguiente
                dron_actual.siguiente = nodo_dron
                nodo_dron.anterior = dron_actual

        # Agregar el sistema a la lista grande que es la lista de sistemas
        lista_sistemas_drones.agregar(nodo_sistema)

    return lista_sistemas_drones

def imprimir_tabla(lista_sistemas_drones):
    resultado = ""

    sistema_actual = lista_sistemas_drones.cabecera
    while sistema_actual:
        resultado += f"Sistema: {sistema_actual.nombre}\n"
        resultado += f"Altura: {sistema_actual.altura_maxima}\n"
        resultado += f"Drones: {sistema_actual.cantidad_drones}\n"

        dron_actual = sistema_actual.cabecera_drones
        fila_encabezado = "\t"
        while dron_actual:
            fila_encabezado += f"{dron_actual.nombre_dron}\t"
            dron_actual = dron_actual.siguiente
        resultado += fila_encabezado + "\n"

        for altura in range(1, sistema_actual.altura_maxima + 1):
            fila_datos = f"{altura}\t"
            dron_actual = sistema_actual.cabecera_drones
            while dron_actual:
                altura_actual = dron_actual.cabecera_alturas
                while altura_actual and altura_actual.valor != altura:
                    altura_actual = altura_actual.siguiente
                if altura_actual:
                    fila_datos += f"{altura_actual.datos}\t"
                else:
                    fila_datos += "\t"
                dron_actual = dron_actual.siguiente
            resultado += fila_datos + "\n"

        sistema_actual = sistema_actual.siguiente

    return resultado


# ------------VERIFICAR QUE LA INFORMACIÓN SE ENCUENTRE JUNTA CON EL DRON, LA ALTURA Y EL SISTEMA
def buscar_sistema_dron_altura(lista_sistemas_drones, nombre_sistema, nombre_dron, valor_altura):
    # BUSCAR EL SISTEMA
    sistema_actual = lista_sistemas_drones.cabecera
    while sistema_actual:
        if sistema_actual.nombre == nombre_sistema:
            # BUSCAR EN LA LISTA DOBLE DEL DRON
            dron_actual = sistema_actual.cabecera_drones
            while dron_actual:
                if dron_actual.nombre_dron == nombre_dron:
                    # BUSCAR EN LA LISTA DE ALTURAS
                    altura_actual = dron_actual.cabecera_alturas
                    while altura_actual:
                        if altura_actual.valor == valor_altura:
                            # SI SE ENCUENTRA, DEVOLVER LOS DATOS
                            return altura_actual.datos
                        altura_actual = altura_actual.siguiente
                dron_actual = dron_actual.siguiente
        sistema_actual = sistema_actual.siguiente

    return None

import os

#**************************** GRAFICO DE LOS SISTEMAS *******************************************
def escribir_dot_sistema(sistema_node):
    dot_code = f'digraph G {{\n'
    dot_code += '  node [shape=plaintext];\n'
    dot_code += f'  label="{sistema_node.nombre}";\n'
    dot_code += '  bgcolor="palegoldenrod";\n'

    dot_code += f'{sistema_node.nombre}  [\n'
    dot_code += f'    label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="5">\n'
    dron_actual = sistema_node.cabecera_drones
    dot_code += '      <tr>\n'
    while dron_actual:
        dot_code += f'        <td bgcolor="lightblue">'
        dot_code += f'{dron_actual.nombre_dron}'
        dot_code += '</td>\n'
            #dron_actual.nombre_dron
        dron_actual = dron_actual.siguiente
    dot_code += '      </tr>\n'
    
    
    for altura in range(1, sistema_node.altura_maxima + 1):


        dron_actual = sistema_node.cabecera_drones
        dot_code += '      <tr>\n'
        while dron_actual:
            dot_code += f'        <td bgcolor="White">'
            altura_actual = dron_actual.cabecera_alturas
            while altura_actual and altura_actual.valor != altura:
                altura_actual = altura_actual.siguiente
            if altura_actual:
                dot_code += f'{altura_actual.datos}'
            dot_code += '</td>\n'
            dron_actual = dron_actual.siguiente

        dot_code += '      </tr>\n'
    dot_code += '    </table>>\n'
    dot_code += '  ];\n'

    dot_code += '}\n'
    return dot_code


def generar_archivo_sistema(lista_sistemas_drones, output_folder):
    sistema_actual = lista_sistemas_drones.cabecera
    while sistema_actual:
        dot_code = escribir_dot_sistema(sistema_actual)
        dot_filename = os.path.join(output_folder, f'{sistema_actual.nombre}.dot')
        with open(dot_filename, 'w') as dot_file:
            dot_file.write(dot_code)
        sistema_actual = sistema_actual.siguiente



#if __name__ == "__main__":
    #xml_file_path = 'C:/Users/natalia/Documents/4sem/ipc2/lab/IPC2_Proyecto2_202200007/entradaV3.xml'
    #lista_sistemas_drones = parse_xml(xml_file_path)
    #imprimir_tabla(lista_sistemas_drones)

    #sistema_name = "SD1"
    #dron_name = "DronX"
    #altura_value = 2

    #data = buscar_sistema_dron_altura(lista_sistemas_drones, sistema_name, dron_name, altura_value)
    #if data is not None:
        #print(f"Sistema: {sistema_name}, Dron: {dron_name}, Altura: {altura_value}: {data}")
    #else:
        #print("NO SE ENCONTRO NADA.")
