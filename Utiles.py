from collections import deque
import re


"""
clase utiles que posee metodos utilizados para ayudar al analizador
"""
class Utilidades:
    @staticmethod
    def es_numero(palabra):
        try:
            float(palabra)
            return True
        except ValueError:
            return False

    @staticmethod
    def corte_palabras(oracion):
        palabras_y_simbolos = re.findall(r'\b\w+\b|\S', oracion)
        return palabras_y_simbolos
