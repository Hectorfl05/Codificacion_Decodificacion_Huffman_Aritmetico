class NodoHuffman:
    def __init__(self, caracter=None, izquierda=None, derecha=None):

        self.caracter = caracter
        self.izquierda = izquierda
        self.derecha = derecha

def reconstruir_arbol_huffman(codigos_huffman, log_file=None):

    raiz = NodoHuffman()  # Nodo raíz del árbol de Huffman

    # Registra en el log el inicio de la reconstrucción
    if log_file:
        log_file.write("Reconstrucción del árbol de Huffman:\n")

    # Inserta cada carácter en el árbol según su código
    for caracter, codigo in codigos_huffman.items():
        nodo_actual = raiz
        for bit in codigo:
            if bit == '0':  # Se mueve a la izquierda para el bit '0'
                if not nodo_actual.izquierda:
                    nodo_actual.izquierda = NodoHuffman()
                nodo_actual = nodo_actual.izquierda
            else:  # Se mueve a la derecha para el bit '1'
                if not nodo_actual.derecha:
                    nodo_actual.derecha = NodoHuffman()
                nodo_actual = nodo_actual.derecha

        # Verifica si el nodo actual es válido
        if nodo_actual is None:
            raise ValueError(f"Error al crear el árbol: nodo actual es None al insertar el carácter '{caracter}' con código {codigo}.")

        # Asigna el carácter al nodo hoja
        nodo_actual.caracter = caracter

        # Registra en el log la inserción del carácter
        if log_file:
            log_file.write(f"Carácter '{caracter}' insertado en el árbol con el código {codigo}.\n")

    # Registra la estructura final del árbol en el log
    if log_file:
        log_file.write("\nEstructura del árbol de Huffman:\n")
        imprimir_arbol_huffman(raiz, log_file)

    return raiz

def imprimir_arbol_huffman(nodo, log_file, nivel=0):

    if nodo is None:
        return

    sangria = "    " * nivel  # Añade sangría para la estructura visual

    if nodo.caracter is not None:
        # Registra un nodo hoja
        log_file.write(f"{sangria}Hoja: Carácter '{nodo.caracter}'\n")
    else:
        # Registra un nodo de decisión
        log_file.write(f"{sangria}Nodo de decisión (bit '0' para la izquierda, bit '1' para la derecha):\n")

        if nodo.izquierda:
            log_file.write(f"{sangria}-0-> Ir a la izquierda\n")
            imprimir_arbol_huffman(nodo.izquierda, log_file, nivel + 1)

        if nodo.derecha:
            log_file.write(f"{sangria}-1-> Ir a la derecha\n")
            imprimir_arbol_huffman(nodo.derecha, log_file, nivel + 1)

def decodificar_huffman(mensaje_codificado, codigos_huffman, log_file=None):

    arbol_huffman = reconstruir_arbol_huffman(codigos_huffman, log_file)

    mensaje_decodificado = []
    nodo_actual = arbol_huffman

    # Registra el inicio del proceso de decodificación
    if log_file:
        log_file.write("\nInicio de la decodificación paso a paso:\n")

    # Procesa cada bit del mensaje codificado
    for i, bit in enumerate(mensaje_codificado):
        if nodo_actual is None:
            raise ValueError(f"Error en el árbol de Huffman: nodo actual es None al procesar el bit {bit} en la posición {i+1}. Verifica la estructura del árbol.")

        # Se mueve a la izquierda o derecha según el bit
        if bit == '0':
            log_file.write(f"Bit {i+1}: {bit} -> Nos movemos a la izquierda.\n")
            nodo_actual = nodo_actual.izquierda
        else:
            log_file.write(f"Bit {i+1}: {bit} -> Nos movemos a la derecha.\n")
            nodo_actual = nodo_actual.derecha

        # Si encontramos un carácter, se agrega al mensaje decodificado
        if nodo_actual.caracter is not None:
            mensaje_decodificado.append(nodo_actual.caracter)
            log_file.write(f"  -> Carácter decodificado: '{nodo_actual.caracter}' encontrado.\n")
            nodo_actual = arbol_huffman  # Reinicia para el siguiente carácter

    # Une los caracteres para formar el mensaje decodificado
    return ''.join([caracter if caracter != '' else ' ' for caracter in mensaje_decodificado])

def registrar_log_proceso(nombre_archivo_log, nombre_archivo, codigos_huffman, mensaje_codificado):

    with open(nombre_archivo_log, 'w') as log_file:
        # Registra la tabla de frecuencias en el log
        log_file.write("Tabla de frecuencias (basada en los códigos de Huffman):\n")
        for caracter, codigo in codigos_huffman.items():
            log_file.write(f"Carácter: {caracter}, Código: {codigo}\n")
        log_file.write("\n")

        # Decodifica el mensaje y registra el proceso
        mensaje_decodificado = decodificar_huffman(mensaje_codificado, codigos_huffman, log_file)

        # Guarda el mensaje decodificado en un archivo
        with open(nombre_archivo, 'w') as result_file:
            result_file.write(f"Mensaje decodificado: {mensaje_decodificado}\n")
            result_file.write(f"Método: Huffman\n")

        # Registra el mensaje decodificado en el log
        log_file.write("\nMensaje decodificado: " + mensaje_decodificado + "\n")
        log_file.write("\nProceso completado con éxito.\n")

    return mensaje_decodificado

def leer_archivo_huffman(nombre_archivo):

    codigos_huffman = {}
    mensaje_codificado = ""
    tasa_compresion = None

    # Lee todas las líneas del archivo
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    # Procesa cada línea del archivo
    seccion = None  # Indica la sección actual del archivo
    for linea in lineas:
        linea = linea.strip()

        if "Tabla de frecuencias:" in linea:
            seccion = "frecuencias"

        elif "Códigos de Huffman:" in linea:
            seccion = "codigos"

        elif "Mensaje codificado:" in linea:
            mensaje_codificado = linea.split(":")[1].strip()

        elif "Tasa de compresión:" in linea:
            tasa_compresion = float(linea.split(":")[1].strip())

        elif seccion == "codigos" and linea:
            # Leer cada línea de código de Huffman
            caracter, codigo = linea.split(":")
            caracter = caracter.strip()
            codigo = codigo.strip()
            codigos_huffman[caracter] = codigo

    return codigos_huffman, mensaje_codificado, tasa_compresion

def Decodification_Huffman(file, num_log):

    name_file = file
    name_file_log = f'ProcesoDecodificacion\\decodificacionProceso{num_log}.txt'
    name_file_result = f'decodificacion\\decodificacion{num_log}.txt'

    # Lee el archivo que contiene la información de Huffman
    codigos_huffman, mensaje_codificado, tasa_compresion = leer_archivo_huffman(name_file)

    # Registra el proceso de decodificación en el archivo log
    message = registrar_log_proceso(name_file_log, name_file_result, codigos_huffman, mensaje_codificado)

    print(f"El proceso de decodificación se ha registrado en {name_file_log}")

    #Retorna el mensaje decodificado
    return message
