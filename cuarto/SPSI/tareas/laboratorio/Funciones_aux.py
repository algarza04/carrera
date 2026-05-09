# FUNCIONES_AUX.PY
# 
# Funciones auxiliares para análisis criptográfico del cifrado de Vigenère.
# Incluye herramientas estadísticas basadas en frecuencias de letras en español,
# cálculo del índice de coincidencia (IC), test chi-cuadrado, y utilidades
# matemáticas para el criptoanálisis. Estas funciones son la base para los
# métodos de Kasiski e Índice de Coincidencia.

import math

# Frecuencias esperadas de letras en español (%)
FRECUENCIAS_ESPANOL = {
    'E': 13.68, 'A': 12.53, 'O': 8.68, 'S': 7.98, 'R': 6.87,
    'N': 6.71, 'I': 6.25, 'D': 5.86, 'L': 4.97, 'C': 4.68,
    'T': 4.63, 'U': 3.93, 'M': 3.15, 'P': 2.51, 'B': 1.42,
    'G': 1.01, 'V': 0.90, 'Y': 0.90, 'Q': 0.88, 'H': 0.70,
    'F': 0.69, 'Z': 0.52, 'J': 0.44, 'X': 0.22, 'W': 0.02,
    'K': 0.01
}

# Índice de coincidencia esperado en español
IC_ESPANOL = 0.0775
IC_ALEATORIO = 0.0385

# Convierte texto a mayúsculas y elimina caracteres no alfabéticos y espacios
def normalizar_texto(msj):
    return ''.join(c.upper() for c in msj if c.isalpha())

# Cuenta la frecuencia de cada elemento en una lista
def contar_elementos(lista):
    recuento = {}
    for elemento in lista:
        recuento[elemento] = recuento.get(elemento, 0) + 1
    return recuento

# Calcula frecuencias absolutas de cada letra en el texto
def calcular_frecuencias(msj):
    msj = normalizar_texto(msj)
    return contar_elementos(msj)

# Calcula frecuencias relativas (porcentaje) de cada letra
def calcular_frecuencias_relativas(msj):
    frecuencias = calcular_frecuencias(msj)
    total = sum(frecuencias.values())
    
    if total == 0:
        return {}
    
    frecuencias_relativas = {}
    for letra, count in frecuencias.items():
        frecuencias_relativas[letra] = (count / total) * 100

    return frecuencias_relativas


# Calcula el índice de coincidencia (IC) de un texto
# Fórmula: IC = Σ(ni * (ni-1)) / (N * (N-1))
# Mide la probabilidad de que dos letras elegidas al azar sean iguales
def indice_coincidencia(msj):
    msj = normalizar_texto(msj)
    N = len(msj)
    
    if N <= 1:
        return 0.0
    
    frecuencias = contar_elementos(msj)
    suma = 0
    for f in frecuencias.values():
        suma += f * (f - 1)
    
    denominador = N * (N - 1)
    return suma / denominador


# Calcula el índice de coincidencia mutua (ICM) entre dos textos
# Fórmula: ICM = Σ(ni * mi) / (N * M)
# Mide la correlación de frecuencias entre dos textos
def indice_coincidencia_mutua(msj1, msj2):
    msj1 = normalizar_texto(msj1)
    msj2 = normalizar_texto(msj2)
    
    N = len(msj1)
    M = len(msj2)
    
    if N == 0 or M == 0:
        return 0.0
    
    freq1 = contar_elementos(msj1)
    freq2 = contar_elementos(msj2)
    
    suma = 0
    for letra in set(freq1) | set(freq2):
        suma += freq1.get(letra, 0) * freq2.get(letra, 0)
    
    return suma / (N * M)


# Calcula el test chi-cuadrado para comparar frecuencias observadas con las esperadas en español
# Fórmula: χ² = Σ((observado - esperado)² / esperado)
# Un valor bajo indica que el texto tiene distribución de frecuencias similar al español
def chi_cuadrado(msj):
    freq_observadas = calcular_frecuencias_relativas(msj)
    
    chi2 = 0.0
    for letra in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observada = freq_observadas.get(letra, 0)
        esperada = FRECUENCIAS_ESPANOL.get(letra, 0.01)
        
        if esperada > 0:
            chi2 += ((observada - esperada) ** 2) / esperada
    
    return chi2


# Divide el texto en grupos según la longitud de clave
# Cada grupo contiene las letras cifradas con la misma posición de clave
def dividir_en_grupos(msj, longitud_clave):
    msj = normalizar_texto(msj)
    grupos = []
    for i in range(longitud_clave):
        grupos.append('')
    
    for i, char in enumerate(msj):
        grupos[i % longitud_clave] += char
    
    return grupos


# Calcula el máximo común divisor usando el algoritmo de Euclides
def calcular_mcd(n1, n2):
    while n2:
        n1, n2 = n2, n1 % n2
    return n1

# Calcula el mínimo común múltiplo
def calcular_mcm(n1, n2):
    return abs(n1 * n2) // calcular_mcd(n1, n2)

# Encuentra todos los factores de un número hasta un máximo
def factores(n, max_factor=None):
    if max_factor is None:
        max_factor = n
    
    factores_lista = []
    for i in range(1, min(int(math.sqrt(n)) + 1, max_factor + 1)):
        if n % i == 0:
            factores_lista.append(i)
            if i != n // i and n // i <= max_factor:
                factores_lista.append(n // i)
    
    return sorted(factores_lista)

# Muestra una tabla de frecuencias del texto
def imprimir_tabla_frecuencias(msj):
    freq = calcular_frecuencias_relativas(msj)
    
    print("\n--- Frecuencias del texto ---")
    for letra in sorted(freq.keys()):
        print(f"{letra}: {freq[letra]:>6.2f}%")
    print()

# Formatea texto en líneas de ancho especificado
def formatear_texto(msj, ancho=60):
    lineas = []
    for i in range(0, len(msj), ancho):
        lineas.append(msj[i:i+ancho])
    return '\n'.join(lineas)

# Muestra el mensaje descifrado con su clave
def imprimir_mensaje_descifrado(mensaje, k):
    print("\n--- Mensaje descifrado ---")
    print(f"Clave: {k}")
    print(formatear_texto(mensaje, 66))
    print()

# Convierte un número de desplazamiento (0-25) a su letra correspondiente (A-Z)
def desplazamiento_a_letra(desplazamiento):
    return chr((desplazamiento % 26) + ord('A'))

# Convierte una letra (A-Z) a su desplazamiento numérico (0-25)
def letra_a_desplazamiento(letra):
    return ord(letra.upper()) - ord('A')
