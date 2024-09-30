import heapq
from collections import Counter
import os

# Nodo del árbol de Huffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    # Comparación basada en la frecuencia (para utilizar en la cola de prioridad)
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función para construir el árbol de Huffman
def construir_arbol_huffman(frecuencias, file):
    heap = []

    # Crea nodos hoja para cada carácter y añadirlos a la cola de prioridad (heap)
    for caracter, frecuencia in frecuencias.items():
        heapq.heappush(heap, NodoHuffman(caracter, frecuencia))

    # Escribe una explicación inicial en el log
    with open(file, 'a') as log:

        log.write("Proceso de Compresion con Huffman\n\n")
        log.write("Paso 1: Tabla de Frecuencias\n")
        log.write("Cada caracter del mensaje tiene una frecuencia asociada, que indica cuantas veces aparece.\n")
        log.write("A continuacion, se muestra una tabla con cada caracter y su frecuencia:\n\n")\

        for caracter, frecuencia in frecuencias.items():
            log.write(f"{caracter}: {frecuencia}\n")
        log.write("\nPaso 2: Seleccion y Reordenamiento de Nodos\n\n")
        log.write("Se seleccionan los dos caracteres con menor frecuencia para combinarlos en un nodo nuevo.\n")
        log.write("Este proceso se repite hasta que solo quede un nodo, que sera la raiz del arbol de Huffman.\n")

    # Construye el árbol de Huffman
    while len(heap) > 1:
        # Extrae los dos nodos con menor frecuencia
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)

        caracter_combinado = nodo1.caracter + nodo2.caracter

        # Crea un nuevo nodo combinado
        nuevo_nodo = NodoHuffman(caracter_combinado, nodo1.frecuencia + nodo2.frecuencia)
        nuevo_nodo.izquierda = nodo1
        nuevo_nodo.derecha = nodo2

        # Añade el nuevo nodo de nuevo al heap
        heapq.heappush(heap, nuevo_nodo)

        # Explica el proceso de selección y fusión en el log
        with open(file, 'a') as log:
            log.write(f"Seleccionados los caracteres con las frecuencias mas bajas:\n")
            log.write(f"1) ({nodo1.caracter}, frecuencia: {nodo1.frecuencia})\n")
            log.write(f"2) ({nodo2.caracter}, frecuencia: {nodo2.frecuencia})\n")
            log.write(f"Estos se combinan en un nuevo nodo con frecuencia {nuevo_nodo.frecuencia}, que representa la suma de ambas frecuencias.\n\n")

    # El nodo restante es la raíz del árbol de Huffman
    return heap[0]

# Función para generar los códigos binarios desde el árbol de Huffman
def generar_codigos_huffman(raiz, codigo_actual, codigos, file):

    if raiz is None:
        return

    # Si es una hoja, asigna el código binario
    if len(raiz.caracter) == 1:
        codigos[raiz.caracter] = codigo_actual

        # Registra en el log el código generado para este carácter
        with open(file, 'a') as log:
            log.write(f"El caracter '{raiz.caracter}' ha sido asignado al codigo binario: {codigo_actual}\n\n")
        return

    # Explica que estamos recorriendo el árbol
    with open(file, 'a') as log:
        log.write(f"Recorriendo el arbol: Nodo con frecuencia {raiz.frecuencia}\n")

    # Verifica si hay un hijo izquierdo
    if raiz.izquierda is not None:

        # Recorre el árbol hacia la izquierda (izquierda -> '0')
        with open(file, 'a') as log:
            log.write(f"Moviendonos a la izquierda (asignando '0') desde el nodo {raiz.caracter}\n\n")
        generar_codigos_huffman(raiz.izquierda, codigo_actual + '0', codigos, file)
    else:
        # Si no hay hijo izquierdo, registra en el log
        with open(file, 'a') as log:
            log.write(f"El nodo {raiz.caracter} no tiene hijo izquierdo.\n\n")

    # Verifica si hay un hijo derecho
    if raiz.derecha is not None:
        # Recorre el árbol hacia la derecha (derecha -> '1')
        with open(file, 'a') as log:
            log.write(f"Moviendonos a la derecha (asignando '1') desde el nodo  {raiz.caracter}\n\n")
        generar_codigos_huffman(raiz.derecha, codigo_actual + '1', codigos, file)
    else:
        # Si no hay hijo derecho, registra en el log
        with open(file, 'a') as log:
            log.write(f"El nodo {raiz.caracter1} no tiene hijo derecho.\n\n")

# Función para codificar un mensaje usando los códigos de Huffman
def codificar_mensaje(mensaje, codigos):

    mensaje_codificado = ''.join([codigos[caracter] for caracter in mensaje])
    return mensaje_codificado

# Función para calcular la tasa de compresión
def calcular_tasa_compresion(mensaje_original, mensaje_codificado):

    bits_originales = len(mensaje_original) * 8  # Cada carácter tiene 8 bits
    bits_codificados = len(mensaje_codificado)
    tasa = bits_originales / bits_codificados
    return tasa

# Función para generar el archivo de log
def generar_log(metodo, modo, codigos, frecuencias, mensaje_codificado, tasa_compresion, numero_log):

    with open(f"codificacion\codificacion{numero_log}.log", 'w') as archivo_log:

        archivo_log.write(f"Metodo: {metodo}\n")
        archivo_log.write(f"Modo: {modo}\n")
        archivo_log.write("\nTabla de frecuencias:\n")
        for caracter, frecuencia in frecuencias.items():
            archivo_log.write(f"{caracter}: {frecuencia}\n")
        archivo_log.write("\nCódigos de Huffman:\n")
        for caracter, codigo in codigos.items():
            archivo_log.write(f"{caracter}: {codigo}\n")
        archivo_log.write(f"\nMensaje codificado: {mensaje_codificado}\n")
        archivo_log.write(f"Tasa de compresión: {tasa_compresion:.2f}\n")

# Función principal para la compresión automática usando Huffman
def huffman_automatic_compression(numero_log):

    # Solicitar el mensaje al usuario
    mensaje = input("Ingrese el mensaje a comprimir: ")

    os.system("cls")

    # 1. Calcular la tabla de frecuencias
    frecuencias = Counter(mensaje)

    # 2. Construir el árbol de Huffman
    log_process = f"ProcesoCodificacion\codificacionProceso{numero_log}.log"
    raiz = construir_arbol_huffman(frecuencias, log_process)

    # 3. Generar los códigos binarios de Huffman
    codigos = {}
    generar_codigos_huffman(raiz, "", codigos,log_process)

    # 4. Codificar el mensaje
    mensaje_codificado = codificar_mensaje(mensaje, codigos)

    # 5. Calcular la tasa de compresión
    tasa_compresion = calcular_tasa_compresion(mensaje, mensaje_codificado)

    # 6. Mostrar resultados
    print("Metodo: Huffman\n")
    print("Modo: Automatico\n")
    print("Tabla de frecuencias:", dict(frecuencias))
    print("Códigos de Huffman:", codigos)
    print("Mensaje codificado:", mensaje_codificado)
    print(f"Tasa de compresión: {tasa_compresion:.2f}")

    # 7. Generar archivo de log
    generar_log("Huffman", "Automático", codigos, frecuencias, mensaje_codificado, tasa_compresion, numero_log)



# Función principal para la compresión manual usando Huffman
def huffman_manual_compression(numero_log, frecuencias, mensaje):

    # 1. Construir el árbol de Huffman
    log_process = f"ProcesoCodificacion\codificacionProceso{numero_log}.log"
    raiz = construir_arbol_huffman(frecuencias, log_process)

    # 2. Generar los códigos binarios de Huffman
    codigos = {}
    generar_codigos_huffman(raiz, "", codigos,log_process)

    # 3. Codificar el mensaje
    mensaje_codificado = codificar_mensaje(mensaje, codigos)

    # 4. Calcular la tasa de compresión
    tasa_compresion = calcular_tasa_compresion(mensaje, mensaje_codificado)

    # 5. Mostrar resultados
    print("Metodo: Huffman\n")
    print("Modo: Manual\n")
    print("Tabla de frecuencias:", frecuencias)
    print("Codigos de Huffman:", codigos)
    print("Mensaje codificado:", mensaje_codificado)
    print(f"Tasa de compresión: {tasa_compresion:.2f}")

    # 6. Generar archivo de log
    generar_log("Huffman", "Manual", codigos, frecuencias, mensaje_codificado, tasa_compresion, numero_log)

