# KASISKI.PY
#
# Método de Kasiski para criptoanálisis de Vigenère. Busca secuencias repetidas
# en el texto cifrado para estimar la longitud de la clave. La idea es que las
# repeticiones ocurren cuando la misma palabra se cifra con la misma parte de la clave,
# por lo que la distancia entre repeticiones es múltiplo de la longitud de la clave.
# Luego usa análisis de frecuencias para recuperar cada letra de la clave.

from . import Funciones_aux

# Encuentra todas las secuencias repetidas en el texto cifrado
def encontrar_repeticiones(msj, min_long=3, max_long=5):
    
    msj = Funciones_aux.normalizar_texto(msj)
    
    repeticiones = {}

    # Buscar secuencias de diferentes longitudes
    for long_current in range(min_long, max_long + 1):
        for i in range(len(msj) - long_current + 1):
            seq = ""
            # Recorremos las subsecuencias de longitud long_current (en principio de 3 a 5)
            for j in range(long_current):
                seq += msj[i + j]
            # Añadimos la posicion en la que se encuentra la subsecuencia
            if seq in repeticiones:
                repeticiones[seq].append(i)
            else:
                repeticiones[seq] = [i]

    # Filtramos solo las que aparecen más de una vez
    repeticiones_filtradas = {}
    for seq, pos in repeticiones.items():
        if len(pos) > 1:
            # En repeticiones_filtradas, para una subsecuencia dada, guardamos la lista de posiciones donde aparece
            repeticiones_filtradas[seq] = pos

    return repeticiones_filtradas

# Calcula las distancias entre las posiciones de cada secuencia repetida    
def calcular_distancias(repeticiones):
    distancias = {}
    
    # Para cada secuencia repetida, calculamos las distancias entre sus posiciones
    for seq, posiciones in repeticiones.items():
        dists = []
        # Calculamos las distancias entre cada par de posiciones de una misma subsecuencia
        
        # Se hace en 2 bucles anidados porque queremos obtener las distancias de todas con todas
        for i in range(len(posiciones) - 1):
            for j in range(i + 1, len(posiciones)):
                dists.append(posiciones[j] - posiciones[i])
        distancias[seq] = dists
    
    return distancias

# Estima la longitud de la clave usando el método de Kasiski
def estimar_longitud_clave_kasiski(msj, min_long=3, max_long=7, max_longitud_clave=20):
    # Encontramos repeticiones
    repeticiones = encontrar_repeticiones(msj, min_long, max_long)
    
    # Calculamos distancias
    distancias_dict = calcular_distancias(repeticiones)
    
    # Juntamos todas las distancias en una sola lista
    todas_distancias = []
    for dists in distancias_dict.values():
        todas_distancias += dists
        
    # Contamos los factores de todas las distancias y luego recopilamos todos los factores de estos
    todos_factores = []
    for dist in todas_distancias:
        factores_distancias = Funciones_aux.factores(dist, max_longitud_clave)
        for f in factores_distancias:
            if f > 1:  # De nada serviría guardar el 1 como factor para todos
                todos_factores.append(f)
    
    # Contamos la frecuencia de los factores
    contador_factores = {}
    for factor in todos_factores:
        if factor in contador_factores:
            contador_factores[factor] += 1
        else:
            contador_factores[factor] = 1
    
    # Ordenar por frecuencia (ponemos la más común primero)
    factores_ordenados = sorted(contador_factores.items(), key=lambda x: x[1], reverse=True)
    
    # Devolvemos factores ordenados por frecuencia
    longitudes_probables = []
    for factor_ordenado in factores_ordenados:
        longitudes_probables.append(factor_ordenado[0])
    
    return longitudes_probables

# Encuentra la clave usando el Índice de Coincidencia Mutua con longitudes de Kasiski
def encontrar_clave_kasiski_icm(c, max_longitud=20):

    msj = Funciones_aux.normalizar_texto(c)
    
    # Obtener longitudes probables usando Kasiski
    longitudes_kasiski = estimar_longitud_clave_kasiski(msj, max_longitud_clave=max_longitud)
    
    # Si Kasiski no encuentra nada, usar rango completo
    if not longitudes_kasiski:
        longitudes_kasiski = list(range(2, max_longitud + 1))
    
    # Probar cada longitud con ICM
    mejor_clave = ""
    mejor_puntuacion = float('inf')
    
    for longitud_clave in longitudes_kasiski[:10]:  # Probar top 10 longitudes
        grupos = Funciones_aux.dividir_en_grupos(msj, longitud_clave)
        
        desplazamientos = [0] * longitud_clave
        
        # Encontrar desplazamientos relativos usando ICM
        for i in range(1, longitud_clave):
            mejor_shift = 0
            mejor_icm = 0.0
            
            for shift in range(26):            
                grupo_i_descifrado = ""
                sub_criptograma_actual = grupos[i]
                
                for j in sub_criptograma_actual:
                    c_valor = ord(j) - ord('A')
                    p_valor = c_valor - shift
                    descifrado_num = (p_valor % 26 + 26) % 26
                    descifrado_char = chr(descifrado_num + ord('A'))
                    grupo_i_descifrado += descifrado_char
                                
                icm = Funciones_aux.indice_coincidencia_mutua(grupos[0], grupo_i_descifrado)
                
                if icm > mejor_icm:
                    mejor_icm = icm
                    mejor_shift = shift
            
            desplazamientos[i] = mejor_shift
        
        # Encontrar desplazamiento absoluto del grupo 0
        mejor_shift_absoluto = 0
        mejor_ic = 0.0
        
        for shift in range(26):
            grupo_0_descifrado = ""
            sub_criptograma_actual = grupos[0]
            
            for j in sub_criptograma_actual:
                c_valor = ord(j) - ord('A')
                p_valor = c_valor - shift
                descifrado_num = (p_valor % 26 + 26) % 26
                descifrado_char = chr(descifrado_num + ord('A'))
                grupo_0_descifrado += descifrado_char
            
            ic = Funciones_aux.indice_coincidencia(grupo_0_descifrado)
            
            if ic > mejor_ic:
                mejor_ic = ic
                mejor_shift_absoluto = shift
        
        # Calcular desplazamientos finales
        desplazamientos_finales = []
        for d in desplazamientos:  
            desplazamiento_absoluto = (mejor_shift_absoluto + d) % 26
            desplazamientos_finales.append(desplazamiento_absoluto)

        # Construir la clave
        clave = ""
        for d_num in desplazamientos_finales: 
            clave_char = chr(d_num + ord('A'))
            clave += clave_char
        
        # Descifrar y evaluar
        mensaje_descifrado = ""
        for i, char in enumerate(msj):
            despl = ord(clave[i % len(clave)]) - ord('A')
            mensaje_descifrado += chr(((ord(char) - ord('A') - despl) % 26) + ord('A'))
        
        # Evaluar calidad
        chi2 = Funciones_aux.chi_cuadrado(mensaje_descifrado)
        ic_desc = Funciones_aux.indice_coincidencia(mensaje_descifrado)
        puntuacion = chi2 + abs(ic_desc - Funciones_aux.IC_ESPANOL) * 1000
        
        if puntuacion < mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_clave = clave
    
    return mejor_clave