from collections import deque
import re


class Tabla_Simbolos:
    def __init__(self):
        self.simbolos = {}
        self.funciones = {}
        """
         se creo una clase con dos diccionarios
         para funcion y variable 
        """
    #------ Métodos para variables------------------------------------------------------
    def agregar_simbolo(self, nombre, tipo, valor=None):
        self.simbolos[nombre] = {'tipo': tipo, 'valor': valor}

    def buscar_simbolo(self, nombre):
        return self.simbolos.get(nombre, {'tipo': None, 'valor': None})

    def obtener_nombres(self):
        return list(self.simbolos.keys())

    def obtener_simbolos(self):
        return [(nombre, simbolo['tipo'], simbolo['valor']) for nombre, simbolo in self.simbolos.items()] 
    
    def obtener_tipo(self, nombre):
        simbolo = self.buscar_simbolo(nombre)
        return simbolo['tipo'] if simbolo else None

    def obtener_valor(self, nombre):
        simbolo = self.buscar_simbolo(nombre)
        return simbolo['valor'] if simbolo else None
    
    #----------------------- Métodos para funciones--------------------------------------------------------
    def agregar_funcion(self, nombre, tipo_retorno):
        self.funciones[nombre] = {'tipo_retorno': tipo_retorno}
    def buscar_funcion(self, nombre):
        return self.funciones.get(nombre, {'tipo_retorno': None})

    def obtener_nombres_funciones(self):
        return list(self.funciones.keys())

    def obtener_funciones(self):
        return [(nombre, funcion['tipo_retorno']) for nombre, funcion in self.funciones.items()]

    def obtener_tipo_retorno_funcion(self, nombre):
        funcion = self.buscar_funcion(nombre)
        return funcion['tipo_retorno'] if funcion else None
      