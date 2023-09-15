class nodo_mensaje:
    def __init__(self, nombre_sistema, nombre_mensaje, dron, valor,significado):
        self.nombre_sistema = nombre_sistema
        self.nombre_mensaje = nombre_mensaje
        self.dron = dron
        self.valor = valor
        self.significado = significado
        self.next = None