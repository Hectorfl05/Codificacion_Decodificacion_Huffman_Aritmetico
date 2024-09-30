from codehuffman import huffman_automatic_compression
from codehuffman import huffman_manual_compression
from intarithcode import Int_Arith_Code_Automatic
from intarithcode import Int_Arith_Code_Manual
from decodehuffman import Decodification_Huffman
from intarithdecode import Decodification_arithmetic
import math
from collections import Counter
import os

# Función para solicitar un número entero al usuario y validar su entrada
def solicitar_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            # Limpia la pantalla en caso de error y muestra el mensaje de error
            os.system("cls")
            print("Error: Debe ingresar un número entero válido.")

# Función para solicitar un único carácter al usuario y validar su entrada
def solicitar_caracter(mensaje):
    while True:
        caracter = input(mensaje)
        if len(caracter) == 1:
            return caracter
        else:
            # Limpia la pantalla en caso de error y muestra el mensaje de error
            os.system("cls")
            print("Error: Debe ingresar un único carácter.")

# Función para validar si un archivo existe en la ruta dada
def validar_ruta_archivo(ruta):
    if os.path.isfile(ruta):
        return True
    else:
        # Muestra un mensaje de error si el archivo no existe
        print(f"Error: El archivo en la ruta '{ruta}' no existe.")
        return False

# Función para crear las carpetas necesarias si no existen
def crear_carpetas():
    carpetas = ['codificacion', 'ProcesoCodificacion', 'decodificacion', 'ProcesoDecodificacion']
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

# Función principal del programa
def main():

    # Crea las carpetas necesarias para los archivos de codificación y decodificación
    crear_carpetas()

    while True:
        print("CODIFICACION Y DECODIFICACION DE UN MENSAJE\n")

        try:
            # Solicita la opción del menú principal
            op = int(input("Seleccione una opción:\n1. Comprimir\n2. Descomprimir\n3. Salir\n> "))

        except ValueError:
            # Manejo de errores si la entrada no es un número entero
            print("Error: Debe ingresar un número entero.")
            input("")
            os.system("cls")
            continue

        # Validar si la opción ingresada es 1, 2 o 3
        if op not in [1, 2, 3]:
            print("Error: Opción no válida. Seleccione 1, 2 o 3.")
            input("")
            os.system("cls")
            continue

        # Opción para comprimir
        if op == 1:

            while True:
                try:
                    # Solicitar el método de compresión
                    metodo = int(input("Seleccione el método de compresión:\n1. Huffman\n2. Aritmética\n> "))
                except ValueError:
                    # Manejo de errores si la entrada no es un número entero
                    print("Error: Debe ingresar un número entero.")
                    input("")
                    os.system("cls")
                    continue

                # Validar si el método seleccionado es 1 o 2
                if metodo not in [1, 2]:
                    print("Error: Método no válido. Seleccione 1 o 2.")
                    input("")
                    os.system("cls")
                    continue
                else:
                    break;

            while True:
                try:
                    # Solicitar el modo de compresión
                    modo = int(input("Seleccione el modo:\n1. Automático\n2. Manual\n> "))
                except ValueError:
                    # Manejo de errores si la entrada no es un número entero
                    print("Error: Debe ingresar un número entero.")
                    input("")
                    os.system("cls")
                    continue

                # Validar si el modo seleccionado es 1 o 2
                if modo not in [1, 2]:
                    print("Error: Modo no válido. Seleccione 1 o 2.")
                    input("")
                    os.system("cls")
                    continue

                else:
                    break;

            # Solicitar un número entero para el archivo log
            try:
                numero = solicitar_entero("Ingrese un número entero para el archivo log\n> ")
            except ValueError:
                print("Error: Debe ingresar un número entero.")
                input("")
                os.system("cls")
                continue

            # Si el método es Huffman
            if metodo == 1:

                os.system("cls")

                if modo == 1:
                    # Método de Huffman con compresión automática
                    os.system("cls")
                    huffman_automatic_compression(numero)

                else:
                    # Método de Huffman con compresión manual
                    mensaje = input("Ingrese el mensaje a comprimir: ")
                    n = solicitar_entero("Ingrese el número de caracteres únicos que forman el mensaje\n> ")

                    frecuencias_ingresadas = {}

                    # Solicitar los caracteres y sus frecuencias al usuario
                    for i in range(n):
                        caracter = solicitar_caracter("Ingrese el carácter\n> ")
                        frecuencia = solicitar_entero(f"Ingrese la frecuencia del carácter '{caracter}'\n> ")
                        frecuencias_ingresadas[caracter] = frecuencia

                    os.system("cls")

                    real_frecuencias = Counter(mensaje)

                    # Verificar coherencia entre la tabla proporcionada y el mensaje
                    coincide = True

                    for caracter, frecuencia in real_frecuencias.items():
                        if caracter not in frecuencias_ingresadas:
                            print(f'El carácter: {caracter}, no se encuentra en la tabla de frecuencias ingresada.\n')
                            coincide = False
                        elif frecuencias_ingresadas[caracter] != frecuencia:
                            print(f'La frecuencia del carácter: {caracter}, no coincide. Comparación: proporcionada: {frecuencias_ingresadas[caracter]}, real: {frecuencia}. \n')
                            coincide = False

                    for caracter, frecuencia in frecuencias_ingresadas.items():
                        if caracter not in real_frecuencias:
                            print(f"Error: El carácter '{caracter}' está en la tabla proporcionada pero no aparece en el mensaje\n.")
                            coincide = False

                    # Si las frecuencias coinciden, realizar la compresión
                    if coincide:
                        os.system("cls")
                        huffman_manual_compression(numero, frecuencias_ingresadas, mensaje)
                    else:
                        print("La tabla de frecuencias proporcionada NO es coherente con el mensaje. Por favor, corrija las frecuencias e intente de nuevo.")

            # Si el método es Aritmético
            else:

                os.system("cls")

                if modo == 1:
                    # Método Aritmético con compresión automática
                    os.system("cls")
                    Int_Arith_Code_Automatic(numero)

                else:
                    # Método Aritmético con compresión manual
                    mensaje = input("Ingrese el mensaje a comprimir:\n> ")
                    n = solicitar_entero("Ingrese el número de caracteres únicos en la tabla de frecuencias:\n> ")

                    frecuencias_proporcionadas = {}
                    for i in range(n):
                        simbolo = solicitar_caracter(f"Ingrese el carácter:\n> ")
                        frecuencia = solicitar_entero(f"Ingrese la frecuencia absoluta del carácter '{simbolo}':\n> ")
                        frecuencias_proporcionadas[simbolo] = frecuencia

                    frecuencias_reales = Counter(mensaje)
                    coincide = True

                    # Verifica coherencia entre la tabla de frecuencias y el mensaje
                    for caracter, frecuencia in frecuencias_reales.items():
                        if caracter not in frecuencias_proporcionadas:
                            print(f'El carácter: {caracter}, no se encuentra en la tabla de frecuencias ingresada.\n')
                            coincide = False
                        elif frecuencias_proporcionadas[caracter] != frecuencia:
                            print(f'La frecuencia del carácter: {caracter}, no coincide. Comparación: proporcionada: {frecuencias_proporcionadas[caracter]}, real: {frecuencia}.\n')
                            coincide = False

                    for caracter in frecuencias_proporcionadas:
                        if caracter not in frecuencias_reales:
                            print(f"Error: El carácter '{caracter}' está en la tabla proporcionada pero no aparece en el mensaje.\n")
                            coincide = False

                    T = sum(frecuencias_proporcionadas.values())

                    while True:
                        if coincide:
                            # Solicita el valor de k al usuario, con una validación de su valor mínimo
                            k = solicitar_entero(f"Ingrese el valor de k (debe ser al menos log2(4*T), con T={T}):\n> ")
                            k_min = math.ceil(math.log2(4 * T))

                            if k < k_min:
                                print(f"Error: k debe ser al menos {k_min}. Inténtelo nuevamente.")
                                input("")
                                os.system("cls")
                                continue
                            else:
                                os.system("cls")
                                Int_Arith_Code_Manual(numero, frecuencias_proporcionadas, k, mensaje, T)
                                break
                        else:
                            print("La tabla de frecuencias proporcionada NO es coherente con el mensaje. Por favor, corrija las frecuencias e intente de nuevo.")
                            input("")
                            break

            # Pausa antes de limpiar la pantalla
            input("\nPresione cualquier tecla para continuar...")
            os.system("cls")

        # Opción para descomprimir
        elif op == 2:

            while True:
                try:
                    # Solicita el método de descompresión
                    metodo = int(input("Seleccione el método de descompresión:\n1. Huffman\n2. Aritmética\n> "))
                except ValueError:

                    # Manejo de errores si la entrada no es un número entero
                    print("Error: Debe ingresar un número entero.")
                    input("")
                    os.system("cls")
                    continue

                # Valida si el método seleccionado es 1 o 2
                if metodo not in [1, 2]:
                    print("Error: Método no válido. Seleccione 1 o 2.")
                    input("")
                    os.system("cls")
                    continue
                else:
                    break;

            # Solicita un número entero para el archivo log
            try:
                numero = solicitar_entero("Ingrese un número entero para el archivo log:\n> ")
            except ValueError:
                print("Error: Debe ingresar un número entero.")
                input("")
                os.system("cls")
                continue

            # Si el método es Huffman
            if metodo == 1:
                os.system("cls")
                Decodification_Huffman(numero)

            # Si el método es Aritmético
            else:
                os.system("cls")
                Decodification_arithmetic(numero)

            input("\nPresione cualquier tecla para continuar...")
            os.system("cls")

        # Opción para salir
        elif op == 3:
            break


if __name__ == "__main__":
    main()
