from collections import deque
import re

from Tabla_Simbolos import Tabla_Simbolos
from Utiles import Utilidades

operadores = {
    '+': 'Suma',
    '=': 'igual',
    '-': 'Resta',
    '*': 'Multiplicación',
    '/': 'División',
    '%': 'Módulo',
    '==': 'Igual a',
    '!=': 'Diferente de',
    '<': 'Menor que',
    '>': 'Mayor que',
    '<=': 'Menor o igual que',
    '>=': 'Mayor o igual que',
    '|': 'OR ',
    '<<': 'Desplazamiento izquierdo',
    '>>': 'Desplazamiento derecho'
}
tipos_de_datos = {
     'int':'Entero', 
     'float':'flotante',
       'string':'cadena',
         'void':'void'}
palabras_reservadas = {
    'if': 'if',
    'while': 'bucle while',
}
"""
se crearon los diccionarios de operador,de datos,palabras  y se obtubieron sus repsctivas
llaves                 
"""

operadores_llave=operadores.keys()
tipos_de_datos_llave=tipos_de_datos.keys()
palabras_reservadas_llave=palabras_reservadas.keys()
#-----------------------------------------------------------------






class AnalizadorSemantico:
    """
    Clase que realiza análisis semántico de un código fuente.
    Cabe recalcar que segun el analizador y el leguaje c++ las asignaciones ya sean string , float,void,int tienen 
    que ser estrigtamente en minuscula y ademas que al ser un analizador semantico se tiene se presupone   que el codigo
    esta sintacticamente bien.
    """

    def __init__(self):
        self.tabla_de_simbolos = Tabla_Simbolos()  # Asumo que TablaDeSimbolos es la clase que estás utilizando
        self.utiles=Utilidades()

    def leer_archivo_texto(self, nombre_archivo):
        """
        Lee el contenido de un archivo de texto.
        """
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
            return contenido
        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no se encuentra.")
            return None
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {str(e)}")
            return None

    def analizar_codigo(self, codigo):
     
        """
        Analiza el código dividiéndolo en líneas y llamando al metodo análisis_línea.
        """

        lineas = codigo.split('\n')

        for numero_linea, linea in enumerate(lineas, start=1):
        
            
            self.analizar_linea(linea, numero_linea)


    def analizar_linea(self, linea, numero_linea):
        """
        Para la realizacion del proyecto se analizo como esta estructurado las asignaciones y las funciones.
        Asignacion [1:tipo de declaracion , 2:variable ,3 :=, 4:el valor a asignar] si cumple estos requisitos se guarda en la tabla
        para las funciones se hizo el mismo analisis 1:tipo de dato funcion 2:nombre de funcion 3:parentesis 4: asignaciones sin embargo aqui las asignaciones de los parametros no tienen un = 
        """


        palabras =  self.utiles.corte_palabras(linea.strip())# palabra es linia sin espacios en blanco
        conta = len(palabras)  #contar cuantos caracteres tien la linia palabra
         
        """
        a la linea se le quita los espacios en blanco y se guarda en palabra despues se cuenta cuantras palabras tiene
        y se hace un for para recorrer palabra por palabra la linea para identificar que es cada cosa
        """
        for posicion in range(conta): # este for va desgranando caracter por caracter de la linia palabra
         
            palabra_actual = palabras[posicion].strip()

            """
            Asignacion de un variable
            tipos_de_datos_llave es un dicionario y se pregunta si palabra_actual esta en el diccionario
            utiles.es_numero valida si k es un entero o no 

            """
            if palabra_actual in tipos_de_datos_llave and "=" in palabras: 
                
                if posicion+1<conta and posicion+2<conta:
                    if palabras[posicion+2]=="=" :
                        k= palabras[posicion+3]


                        """
                        se busca saber si palabra actual es un tipo de dato entero y que k sea un numero  o este en la tabla si no
                        es un error asi para los int,float,string 
                        """
                     
                      #  print(self.tabla_de_simbolos.buscar_simbolo(k))
                        if palabra_actual == "int" and ( self.utiles.es_numero(k) or self.tabla_de_simbolos.obtener_tipo(k)=="int"):
                           
                            pos = posicion + 4

                            if pos<conta:
                                for cont in range(pos, len(palabras)):
                                    if palabras[cont] in operadores_llave:
                                        if  ( self.utiles.es_numero(palabras[cont+1]) or self.tabla_de_simbolos.obtener_tipo(palabras[cont+1])=="int"):
                                             
                                            self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabras[posicion],palabras[cont+1])
                                            print(self.tabla_de_simbolos.obtener_valor( palabras[posicion+1]))

                                    
                                        else:
                                            print(f"Error - Línea {numero_linea}: asignacion de tipo de dato   incorrecta")
                            else:
                                self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabras[posicion],palabras[posicion+3])
         

                        elif palabra_actual == "string" and  self.utiles.es_numero(k)==False  and k!="":
                                    
                                pos = posicion + 6
                                total=True

                                if pos<conta:
                                    for cont in range(pos, len(palabras)):
                                        if palabras[cont] in operadores_llave:
                                            
                                            if  ( self.utiles.es_numero(palabras[cont+1]) or self.tabla_de_simbolos.obtener_tipo(palabras[cont+1])!="String"):
                                                  total=False
                                               
                                            

                                    if total:
                                        self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabras[posicion],palabras[cont+1])
                                    else:
                                      print(f"Error - Línea {numero_linea}: asignacion de tipo de dato   incorrecta")     

                                elif  palabras[posicion+1] in self.tabla_de_simbolos.obtener_nombres():
                                    print(f"Error - Línea {numero_linea}: asignacion de tipo de dato   incorrecta")   
                                
                                else:
                                    self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabras[posicion],palabras[posicion+4])

                                    
                                  ##  self.tabla_de_simbolos.agregar_simbolo(palabras[1],palabras[0],palabras[4])
                                    ##print ( self.tabla_de_simbolos.obtener_simbolos())

                        elif palabra_actual == "float" and  self.utiles.es_numero(k) :
                                    self.tabla_de_simbolos.agregar_simbolo(palabras[1],palabras[0],palabras[3])
                        
                        elif palabra_actual == "void" and  self.utiles.es_numero(k)==False  and k!="" or self.utiles.es_numero(k)==True and '(' is not palabras:
                                    print(f"Error - Línea {numero_linea}: tipo de dato '{palabras[posicion].strip()}'  incorrecta")

                        else:
                          
                            print(f"Error - Línea {numero_linea}: tipo de dato '{palabras[posicion].strip()}'  incorrecta")
                                    
                    



               # print(self.tabla_de_simbolos.obtener_simbolos())
           
               

            elif  palabra_actual in self.tabla_de_simbolos.obtener_nombres() and "=" in palabras :  # buscar si la palabra se encuentra en el dicionario y que la linia palabra haya un igual
                     
                """
             si palabra actual esta en el diccionario   se valida si la asignacion que le entra es un tipo de dato valido
             si es entero tiene que ser entero
             o si es string tiene que ser una cadena 
              
                """

                if posicion+1<conta and posicion+2<conta: # valorar si la busqueda es correcta
                    if palabras[posicion+1]=="=" :
                        k= palabras[posicion+2]


                       # print(self.tabla_de_simbolos.obtener_tipo(palabra_actual))
                       
                        if self.tabla_de_simbolos.obtener_tipo(palabra_actual) == "int" or  self.tabla_de_simbolos.obtener_tipo(palabra_actual) == "float":
                            
                            pos = posicion + 3
                            if pos<conta:
                               

                                for cont in range(pos, len(palabras)):
                                    if palabras[cont] in  operadores_llave:
                                            
                                        if  ( self.utiles.es_numero(palabras[cont+1])==False) or (self.tabla_de_simbolos.obtener_tipo(palabras[cont+1])=="string"):
                                              
                                             print(f"Error - Línea {numero_linea}: asignacion de tipo de dato   incorrecta")

                        
                        elif self.tabla_de_simbolos.obtener_tipo(palabra_actual) == "string" :
                            
                            pos = posicion + 3
                            if pos<conta:
                                for cont in range(pos, len(palabras)):
                                    if palabras[cont] in  operadores_llave:
                                            
                                        if  ( self.utiles.es_numero(palabras[cont+1])==True) or ( (self.tabla_de_simbolos.obtener_tipo(palabras[cont+1])=="int")or (self.tabla_de_simbolos.obtener_tipo(palabras[cont+1])=="float") ):
                                              
                                             print(f"Error - Línea {numero_linea}: asignacion de tipo de dato   incorrecta")                    

                        else:
                            print(f"Error - Línea {numero_linea}: asignacion de tipo de dato   incorrecta")          
                                  

                            
                       
                             # si la el dato es un entero y se asigna un string
                        
                        if ((self.tabla_de_simbolos.obtener_tipo(palabra_actual) == "int" )or  self.tabla_de_simbolos.obtener_tipo(palabra_actual) == "float") and k=='"' :
                                print(f"Error - Línea {numero_linea}: Variable '{palabras[posicion].strip()}' asignacion incorrecta")
                                 
                        # si la el dato es un string y se asigna un entero
                             
                        elif self.tabla_de_simbolos.obtener_tipo(palabra_actual) == "string" and  self.utiles.es_numero(k)==True: 
                            print(f"Error - Línea {numero_linea}: Variable '{palabras[posicion].strip()}' asignacion incorrecta")
                             
        

            elif ( palabra_actual is not "") and  ("=" in palabras) and (palabra_actual not in self.tabla_de_simbolos.obtener_nombres()) and (palabra_actual not in palabras_reservadas_llave )and "(" not in palabras :
                
                if posicion+1<conta:
                    if palabras[posicion+1]=="=" :
                        print(f"Error - Línea {numero_linea}: Variable '{palabras[posicion].strip()}' NO ESTA DECLARADO") 



# ----------------------------esto if es de la declaracion de metodos--------------------------------------------

            elif   "(" in palabras and ")" in palabras  :# si en linia palabra se tiene dos parentesis y los pa
                
                """
               aqui se analisa el tipo de dato de la funcion ya sea int ,void,string,float y se ve si existen y tambien el nombre de la 
               funcion
              
                """
                if palabra_actual in tipos_de_datos_llave: # si palabra actual esta en datos 
                    """
                    aqui se analisa el tipo de dato de la funcion ya sea int ,void,string,float y se ve si existen y tambien el nombre de la 
                    funcion
                    si palabra_acutual es un tipo de dato int ,void,string,float y  en la linea palabras se encuenta un ( se guarda en la table
              
                    """
                    if palabra_actual == "int" and  palabras[ posicion+2]== "(":  
                            self.tabla_de_simbolos.agregar_funcion(palabras[1],palabras[0])
                            
       
                    elif palabra_actual == "string" and  palabras[ posicion+2]=="(" :    
                            self.tabla_de_simbolos.agregar_funcion(palabras[1],palabras[0])
                           


                    elif palabra_actual == "float" and  palabras[ posicion+2] =="(": 
                            self.tabla_de_simbolos.agregar_funcion(palabras[1],palabras[0])
                            

                  
                    elif palabra_actual == "void" and  palabras[ posicion+2] =="(": 
                            self.tabla_de_simbolos.agregar_funcion(palabras[1],palabras[0])
                            
            #--------------------------------------------------------------------------------------------- 
                    k= palabras[posicion+2]# asignar en la tabla varaiable que esta en una funcion

                    """
                    
                    si palabra_actual es un tipo de dato int ,void,string,float y k es el valor que esta 2 posiciones despues de palabra actual
                    y marca si se encuenta un ) o una [ , ] para que se valide y se guarde en la tabla
              
                    """
 
                    if palabra_actual == "float" and  (k=="," or k==")"):
                            self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabra_actual,)
                    
                    
                    if palabra_actual == "int" and (k=="," or k==")"):
                            self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabra_actual,)
                            
                    
                    if palabra_actual == "string" and (k=="," or k==")"):
                            self.tabla_de_simbolos.agregar_simbolo(palabras[posicion+1],palabra_actual,)
                    
                    if palabra_actual == "void" and (k=="," or k==")"):  
                          print(f"Error - Línea {numero_linea}: asignacion {palabra_actual}  invalida")
          
            if palabra_actual in palabras_reservadas_llave and "(" in palabras and ")" in palabras  :
                 k= palabras[posicion+2]
                 j=palabras[posicion+4]
                

                 """
                    dentro de los if o while se valora los datos y se busca si hay un arror de asignacion de comparacion
                    de diferente tipo etc
                 """
                # if  self.tabla_de_simbolos.buscar_simbolo(j) and k in self.tabla_de_simbolos.obtener_simbolos:
                 if self.utiles.es_numero(k) and self.utiles.es_numero(j):

                    if "=" in palabras :
                      print(f"Error - Línea {numero_linea}:  aignacion invalida")   
                   
                     
                 elif self.utiles.es_numero(k)==False and self.utiles.es_numero(j)==False:
                     
                     if self.tabla_de_simbolos.obtener_tipo(k) and  self.tabla_de_simbolos.obtener_tipo(j) :
                         print(self.tabla_de_simbolos.obtener_tipo(k))
                         print(self.tabla_de_simbolos.obtener_tipo(j))
                     
                     else:
                         print(f"Error - Línea {numero_linea}:  diferencia de variable")   
                
                 elif  self.utiles.es_numero(k)==False and  self.utiles.es_numero(j)==True:
                    

                    if self.tabla_de_simbolos.obtener_tipo(k)=="string" or self.tabla_de_simbolos.obtener_tipo(k)==None:   
                            print(f"Error - Línea {numero_linea}:  DIFERENCIAS EN LA DECLARACION DE VARIABLES") 
                    
                

                    
                 elif  self.utiles.es_numero(k)==True and  self.utiles.es_numero(j)==False:
                    if self.tabla_de_simbolos.obtener_tipo(j) !="int" :
                        print(f"Error - Línea {numero_linea}:  DIFERENCIAS EN LA DECLARACION DE VARIABLES") 
            
            if palabra_actual == "return" :
                 """
                   en el retur se busca primero obtener en nombre de la funcion en la tabla
                   despues con el nombre de la funcion obtener su tipo de dato ya sea int ,float, string o void
                   y despues ya obtenido estos datos comparar con el dato que le sigue al return valorar si es 
                   int, string ,float 

                 """
                 if conta>1:
                     nombre=self.tabla_de_simbolos.obtener_nombres_funciones()
                     if len(nombre)>0: 

                        if self.tabla_de_simbolos.buscar_funcion(nombre[0])!=None:
                       
                           tipo_funcion=self.tabla_de_simbolos.obtener_tipo_retorno_funcion(nombre[0]) 
                           nombre_retorno=self.tabla_de_simbolos.obtener_tipo(palabras[1])

                           if tipo_funcion !=None and nombre_retorno !=None:
                                
                                if(nombre_retorno!=tipo_funcion): # si son diferentes  el retorno es error
                                    print(f"Error - Línea {numero_linea}:  valor de retorno no coincide con la declaración de funcion")
                          
                           elif  (tipo_funcion=="int" or tipo_funcion=="float") and palabras[1]=='"':
                                print(f"Error - Línea {numero_linea}:  valor de retorno no coincide con la declaración de funcion")
                                                                 
                           elif  tipo_funcion=="String"  and  self.utiles.es_numero(palabras[1]):
                                    print(f"Error - Línea {numero_linea}:  valor de retorno no coincide con la declaración de funcion")

                           elif  tipo_funcion=="void":
                                    print(f"Error - Línea {numero_linea}:  valor de retorno no coincide con la declaración de funcion")


                        else:
                            print(f"Error - Línea {numero_linea}:  valor de retorno no coincide con la declaración de funcion") 

    



        


if __name__ == "__main__":
    a = AnalizadorSemantico()

   
    nombre_archivo = "k.txt"
    nombre_archivo_2 = "m.txt"
    nombre_archivo_3 = "p.txt"

    contenido_codigo = a.leer_archivo_texto(nombre_archivo)
    contenido_codigo_2 = a.leer_archivo_texto(nombre_archivo_2)
    contenido_codigo_3 = a.leer_archivo_texto(nombre_archivo_3)

    print("-------------------------PRIMER METODO K--------------------------------")
    print("       ")

    if contenido_codigo:
        a.analizar_codigo(contenido_codigo)
    else:
        print("No se pudo analizar el código debido a errores en la lectura del archivo.")

    print("-------------------------SEGUNDO METODO m--------------------------------")
    print("       ")

    if contenido_codigo_2:
        a.analizar_codigo(contenido_codigo_2)
    else:
        print("No se pudo analizar el código debido a errores en la lectura del archivo.")


    print("-------------------------TERCER METODO  p--------------------------------")
    print("       ")

    if contenido_codigo_3:
        a.analizar_codigo(contenido_codigo_3)
    else:
        print("No se pudo analizar el código debido a errores en la lectura del archivo.")



    