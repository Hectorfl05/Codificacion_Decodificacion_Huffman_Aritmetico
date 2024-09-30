from numpy import power
import math
import re

# Función para escribir en el archivo .log
def escribir_log(archivo, mensaje):
    with open(archivo, 'a') as log:
        log.write(mensaje + '\n')

# Función para extraer valores del archivo de log
def extraer_valores_log(log_file):

    with open(log_file, 'r') as log:
        contenido = log.read()  # Lee el contenido del archivo

        # Extrae la tabla de frecuencias
        frecuencias = re.findall(r"\('(.+)', (\d+), (\d+), (\d+)\)", contenido)

        frecuencias = [(simbolo, int(frecuencia), int(f_i), int(f_i1)) for simbolo, frecuencia, f_i, f_i1 in frecuencias]

        # Extrae valor de K
        k_match = re.search(r"Valor de K: (\d+)", contenido)
        k = int(k_match.group(1)) if k_match else None

        # Extrae valor de T
        T_match = re.search(r"Valor de T: (\d+)", contenido)
        T = int(T_match.group(1)) if T_match else None

        # Extrae valor de n
        n_match = re.search(r"Valor de n: (\d+)", contenido)
        n = int(n_match.group(1)) if n_match else None

        # Extrae los bits codificados
        bits_match = re.search(r"Bits codificados: \[([01, ]+)\]", contenido)
        bits = [int(b) for b in bits_match.group(1).split(", ")] if bits_match else []

        return frecuencias, k, T, n, bits

# Decodificación aritmética con registro
def IntArithDecode(bits, k, n, frecuencias, T, log_resultado, log_explicacion):
    R = power(2, k)
    l = 0
    u = R - 1

    escribir_log(log_explicacion, f"Valor inicial de l = {l}, u = {u}, R = {R}\n")

    # Función para obtener el símbolo a partir de z
    def get_symbol(z):
        for mj, c, f_i, f_i1 in frecuencias:
            if f_i <= z < f_i1:
                return mj
        raise ValueError(f"No se encontró el símbolo para z = {z}")

    # Función para obtener f(i)
    def fi(vi):
        for mj, c, f_i, f_i1 in frecuencias:
            if vi == mj:
                return f_i
        raise ValueError(f"Símbolo {vi} no encontrado")

    # Función para obtener f(i+1)
    def fi_plus1(vi):
        for mj, c, f_i, f_i1 in frecuencias:
            if vi == mj:
                return f_i1
        raise ValueError(f"Símbolo {vi} no encontrado")

    mensaje_decodificado = []
    z = 0

    # Convertimos los primeros k bits a un valor decimal
    escribir_log(log_explicacion, f"Convertir los primeros {k} bits a valor decimal:")
    for i in range(k):
        z = 2 * z + bits[i]
        escribir_log(log_explicacion, f"Bit {i + 1} = {bits[i]} => z = {z}")

    i = k  # Empezamos a leer desde el bit k
    escribir_log(log_explicacion, f"Valor inicial de z después de leer los primeros {k} bits: z = {z}\n")

    while len(mensaje_decodificado) < n:
        s = u - l + 1
        freq_z = math.floor(((z - l + 1) * T - 1) / s)

        # Identifica el símbolo correspondiente a freq_z
        vi = get_symbol(freq_z)
        mensaje_decodificado.append(vi)
        escribir_log(log_explicacion, f"Encontrado símbolo '{vi}' para freq_z = {freq_z}")

        # Ajusta los límites
        u_prev, l_prev = u, l
        u = l + math.floor(s * fi_plus1(vi) / T) - 1
        l = l + math.floor(s * fi(vi) / T)
        escribir_log(log_explicacion, f"Ajuste de límites: l = {l_prev} => {l}, u = {u_prev} => {u}, s = {s}\n")

        # Ajusta z, l y u según las reglas de reescalado
        while True:
            if u < R / 2:
                escribir_log(log_explicacion, f"Regla Inferior aplicada (u < R/2): u = {u}, l = {l}.")
            elif l >= R / 2:
                z = z - R / 2
                l = l - R / 2
                u = u - R / 2
                escribir_log(log_explicacion, f"Regla Superior aplicada (l >= R/2): l = {l}, u = {u}, z = {z}.")
            elif l >= R / 4 and u < 3 * R / 4:
                z = z - R / 4
                l = l - R / 4
                u = u - R / 4
                escribir_log(log_explicacion, f"Regla Medio aplicada (R/4 <= l < 3R/4): l = {l}, u = {u}, z = {z}.")
            else:
                break

            l = 2 * l
            u = 2 * u + 1
            if i < len(bits):
                z = 2 * z + bits[i]
            else:
                z = 2 * z  # Si no quedan más bits, asumimos 0
            i += 1
            escribir_log(log_explicacion, f"Nuevo z = {z}, l = {l}, u = {u} después de escalado.\n")

    # Guarda el mensaje decodificado
    escribir_log(log_explicacion, f"Mensaje final decodificado: {''.join(mensaje_decodificado)}")
    escribir_log(log_resultado, f"Mensaje decodificado: {''.join(mensaje_decodificado)}")
    escribir_log(log_resultado, f"Por el método: Aritmético")

    #Une los carácteres del mensaje decodificado
    return ''.join(mensaje_decodificado)


def Decodification_arithmetic(code_file, num_log):

    #Inicializacion de los archivos.log
    log = code_file
    log_resultado = f'decodificacion/decodificacion{num_log}.log'
    log_explicacion = f'ProcesoDecodificacion/decodificacionProceso{num_log}.log'

    # Extrae valores del archivo de log original
    frecuencias, k, T, n, bits = extraer_valores_log(log)

    #Llamada a la función de decodificación con registro
    mensaje_decodificado = IntArithDecode(bits, k, n, frecuencias, T, log_resultado, log_explicacion)

    print(f"El proceso de decodificación se ha registrado en {log_explicacion}")

    #Retorna el mensaje decodificado
    return mensaje_decodificado




