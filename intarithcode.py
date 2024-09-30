from numpy import power
import math
from collections import Counter
import os


def escribir_log(archivo, mensaje):
    # Función para escribir mensajes en un archivo de log
    with open(archivo, 'a') as log:
        log.write(mensaje + '\n')


# Codificación aritmética
def IntArithCode(mensaje, k, n, log_archivo, log_resultado, T, fi):
    R = power(2, k)  # Cálculo de R como 2 elevado a la k
    l = 0  # Límite inferior inicial
    u = R - 1  # Límite superior inicial
    m = 0  # Contador de bits
    i = 1  # Contador de iteraciones
    bits = []  # Lista para almacenar los bits codificados
    it = 0  # Contador de iteraciones

    # Paso 1: Genera la tabla de frecuencias acumuladas
    frecuencias = []
    acumulada = 0

    # Genera frecuencias acumuladas
    for simbolo, frecuencia in sorted(fi.items(), key=lambda x: x[0]):
        frecuencias.append((simbolo, frecuencia, acumulada, acumulada + frecuencia))
        acumulada += frecuencia

    # Muestra la tabla de frecuencias
    print("Tabla de frecuencias: (mj, c, fi, fi + 1 )")
    escribir_log(log_archivo, "Tabla de frecuencias:")
    escribir_log(log_resultado, "Tabla de frecuencias:")

    # Escribe y muestra la tabla de frecuencias
    for f in frecuencias:
        escribir_log(log_archivo, f"{f}")
        escribir_log(log_resultado, f"{f}")
        print(f)

    # Muestra y registra valores de k, T, n y R
    escribir_log(log_archivo, f" \n Valor de K: {k}")
    escribir_log(log_resultado, f" \n Valor de K: {k}")
    print(f" \n Valor de K: {k}")

    escribir_log(log_archivo, f" \n Valor de T: {T}")
    escribir_log(log_resultado, f" \n Valor de T: {T}")
    print(f" \n Valor de T (Sumatoria de las frecuencias absolutas): {T}")

    escribir_log(log_archivo, f" \n Valor de n: {n}\n")
    escribir_log(log_resultado, f" \n Valor de n: {n}\n")
    print(f" \n Valor de n (Tamaño del mensaje): {n}\n")

    escribir_log(log_archivo, f" \n Valor de R (2^k): {R}\n")

    # Función para obtener la frecuencia acumulada de un símbolo
    def fi(vi):
        for mj, c, f_i, f_i1 in frecuencias:
            if vi == mj:
                return f_i
        raise ValueError(f"Símbolo {vi} no encontrado")

    # Función para obtener la frecuencia acumulada del siguiente símbolo
    def fi_plus1(vi):
        for mj, c, f_i, f_i1 in frecuencias:
            if vi == mj:
                return f_i1
        raise ValueError(f"Símbolo {vi} no encontrado")

    # Función para escribir un bit en la lista
    def WriteBit(bit):
        bits.append(bit)

    # Itera sobre cada símbolo del mensaje
    for i in range(1, n + 1):
        vi = mensaje[i - 1]  # Símbolo actual
        s = u - l + 1  # Tamaño del rango
        u = l + math.floor(s * fi_plus1(vi) / T) - 1  # Actualiza el límite superior
        l = l + math.floor(s * fi(vi) / T)  # Actualiza el límite inferior

        # Explicación del ajuste del rango
        explicacion = (f'Ajuste del rango para el símbolo vi = "{vi}":\n'
                       f'1. Se calcula el tamaño del rango: s = u - l + 1, obteniendo s = {s}.\n'
                       f'2. Se actualiza el límite superior: u = l + floor(s * f(vi+1) / T) - 1, nuevo u = {u}.\n'
                       f'3. Se actualiza el límite inferior: l = l + floor(s * f(vi) / T), nuevo l = {l}.\n'
                       f'El rango se ajusta para representar con precisión el símbolo vi y reducir el espacio de codificación.\n')

        escribir_log(log_archivo, f'{explicacion}')

        # Ajusta el rango según las reglas
        while True:
            if l >= R / 2:
                it += 1
                explicacion = (f'Iteración {it}: l={l}, u={u}, s={s}, m={m}, Regla utilizada:'
                               f'Regla Superior aplicada R/2 = {R/2}: Se escribe el bit 1, se aplica la transformación para ajustar el rango.\n'
                               f'Los nuevos valores son: l = 2*l - R = {2*l - R}, u = 2*u - R + 1 = {2*u - R + 1}.\n'
                               f'Se escribe el bit 0, {m} veces, y luego se resetea el contador m a 0\n')

                WriteBit(1)  # Escribe bit 1
                u = 2 * u - R + 1  # Ajusta u
                l = 2 * l - R  # Ajusta l
                for j in range(1, m + 1):
                    WriteBit(0)  # Escribe m veces bits 0
                m = 0  # Reinicia contador

                escribir_log(log_archivo, f'{explicacion}')

            elif u < R / 2:
                it += 1
                explicacion = (f'Iteración {it}: l={l}, u={u}, s={s}, m={m}, Regla utilizada:'
                               f'Regla Inferior aplicada R/2 = {R/2}: Se escribe el bit 0, se aplica la transformación para ajustar el rango.\n'
                               f'Los nuevos valores son: l = 2*l = {2*l}, u = 2*u + 1 = {2*u + 1}.\n'
                               f'Se escribe el bit 1, {m} veces, y luego se resetea el contador m a 0\n')
                WriteBit(0)  # Escribi bit 0
                u = 2 * u + 1  # Ajusta u
                l = 2 * l  # Ajusta l
                for j in range(1, m + 1):
                    WriteBit(1)  # Escribe m veces bits 1

                m = 0  # Reinicia contador

                escribir_log(log_archivo, f'{explicacion}')

            elif l >= R / 4 and u < 3 * R / 4:
                it += 1
                explicacion = (f'Iteración {it}: l={l}, u={u}, s={s}, m={m}, Regla utilizada:'
                               f'Regla Medio aplicada R/4 = {R/4} y 3R/4 = {3 * R / 4}:\n '
                               f'Se ajusta el rango intermedio: l = 2*l - R/2 = {2*l - R/2}, u = 2*u - R/2 + 1 = {2*u - R/2 + 1}.\n'
                               f'Se aumenta en 1 el contador m\n.')

                u = 2 * u - R / 2 + 1  # Ajusta u
                l = 2 * l - R / 2  # Ajusta l
                m += 1  # Aumenta contador

                escribir_log(log_archivo, f'{explicacion}')

            else:
                break

    # Determina el último bit a escribir según el rango
    if l >= R / 4:
        explicacion = (f'Debido a que l >= R/4 ({l} >= {R/4}), se escribe el bit 1. \n'
                       f'Luego, se escribe el bit 0 las veces que contiene el contador m, en este caso {m}.\n'
                       f'Y por último, se escribe el bit 0.')
    else:
        explicacion = (f'Debido a que l < R/4 ({l} < {R/4}), se escribe el bit 0. \n'
                       f'Luego, se escribe el bit 1 las veces que contiene el contador m, en este caso {m}.\n'
                       f'Y por último, se escribe el bit 1.')

    escribir_log(log_archivo, f'{explicacion}')

    # Escribe el último bit y los bits de acuerdo al contador
    if l >= R / 4:
        WriteBit(1)  # Escribe bit 1
        for j in range(1, m + 1):
            WriteBit(0)  # Escribe m veces bits 0
    else:
        WriteBit(0)  # Escribe bit 0
        for j in range(1, m + 1):
            WriteBit(1)  # Escribir m veces bits 1

    # Guarda los bits codificados en el log de resultados
    escribir_log(log_resultado, f'\nMensaje codificado: {bits}\n')

    return bits  # Retorna los bits codificados



# Función para codificación automática
def Int_Arith_Code_Automatic(num_log):

    #Solicita el mensaje al usuario
    mensaje = input("Ingrese el mensaje a comprimir:\n> ")

    os.system("cls")

    # Paso 1: Contar frecuencias de cada símbolo en el mensaje
    frecuencias_absolutas = Counter(mensaje)
    T = sum(frecuencias_absolutas.values())  # Total de frecuencias

    # Paso 2: Calcular k automáticamente usando la fórmula k = ⌈log2(4T)⌉
    k = math.ceil(math.log2(4 * T))

    # Paso 3: Longitud del mensaje
    n = len(mensaje)

    # Paso 4: Creación de los archivos log
    log_process = f"ProcesoCodificacion\codificacionProceso{num_log}.log"

    log_results = f"codificacion\codificacion{num_log}.log"

   #Se indica el método y el modo de codificación

    print("Metodo: Aritmetico\n")
    print("Modo: Automatico\n")

    escribir_log(log_results, f'Metodo: Aritmetico')

    escribir_log(log_results, f'Modo: Automático\n')

    # Paso 5: Codificar el mensaje
    bits_codificados = IntArithCode(mensaje, k, n, log_process, log_results, T, frecuencias_absolutas)

    #Imprime el resultado final
    print("Bits codificados:", bits_codificados)

    escribir_log(log_results, f'Bits codificados: {bits_codificados}')



# Función para codificación automática
def Int_Arith_Code_Manual(num_log,frecuencias,k, mensaje,T):

    #Paso 1: Calcular el tamaño del mensaje
    n = len(mensaje)

    # Paso 2: Creación de los archivos log
    log_process = f"ProcesoCodificacion\codificacionProceso{num_log}.log"

    log_results = f"codificacion\codificacion{num_log}.log"

    #Se indica el método y el modo de codificación

    print("Metodo: Aritmetico\n")
    print("Modo: Manual\n")

    escribir_log(log_results, f'Metodo: Aritmetico')

    escribir_log(log_results, f'Modo: Automático\n')

    # Paso 3: Codificar el mensaje
    bits_codificados = IntArithCode(mensaje, k, n, log_process, log_results, T, frecuencias)

    #Imprime el resultado final
    print("Bits codificados:", bits_codificados)

    escribir_log(log_results, f'Bits codificados: {bits_codificados}')



