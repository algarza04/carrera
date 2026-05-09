from . import Funciones_aux

# Estima la longitud de la clave usando el método del Índice de Coincidencia
def estimar_longitud_clave_ic(c, max_longitud=20):
    # aceptamos solo letras, las cinvertimos en mayusculas y limpiamos espacios
    msj = Funciones_aux.normalizar_texto(c)
    resultados = []
    
    # iteramos sobre las posibles longitudes
    for longitud in range(1, max_longitud + 1):
        # dividimos en grupos de longitud estimada
        grupos = Funciones_aux.dividir_en_grupos(msj, longitud)
        
        ics = []
        for grupo in grupos:
            if len(grupo) > 1:
                ic = Funciones_aux.indice_coincidencia(grupo)
                ics.append(ic)
        
        if not ics:
            continue
        
        ic_promedio = sum(ics) / len(ics)
        diferencia = abs(ic_promedio - Funciones_aux.IC_ESPANOL)
        
        resultados.append({
            'longitud': longitud,
            'diferencia': diferencia
        })
        
    resultados.sort(key=lambda x: x['diferencia'])
    
    return resultados[0]['longitud']

# Encuentra la clave usando el Índice de Coincidencia Mutua
def encontrar_clave_ic_mutua(c, longitud_clave):
    msj = Funciones_aux.normalizar_texto(c)
    grupos = Funciones_aux.dividir_en_grupos(msj, longitud_clave)
    
    desplazamientos = [0] * longitud_clave
    
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
    
    desplazamientos_finales = []

    for d in desplazamientos:  
        desplazamiento_absoluto = (mejor_shift_absoluto + d) % 26
        
        desplazamientos_finales.append(desplazamiento_absoluto)

    clave = ""

    for d_num in desplazamientos_finales: 
        clave_char = chr(d_num + ord('A'))
        
        clave += clave_char
        
    # clave contiene la clave descifrada
    return clave

# Encuentra la clave mediante análisis de frecuencias
def encontrar_clave_por_frecuencias(c, longitud_clave):
    msj = Funciones_aux.normalizar_texto(c)
    clave = []

    
    grupos = Funciones_aux.dividir_en_grupos(msj, longitud_clave)
    
    for pos in range(longitud_clave):
        grupo = grupos[pos]
        
        mejor_letra = 'A'
        mejor_puntuacion = float('inf')
        mejor_ic = 0.0
        
        for shift in range(26):
            descifrado = ""
            
            for j in grupo:
                j_valor = ord(j) - ord('A')
                
                p_valor = j_valor - shift
                
                descifrado_num = (p_valor % 26 + 26) % 26

                descifrado_char = chr(descifrado_num + ord('A'))
                
                descifrado += descifrado_char
                
            
            chi2 = Funciones_aux.chi_cuadrado(descifrado)
            ic = Funciones_aux.indice_coincidencia(descifrado)
            
            ic_normalizado = abs(ic - Funciones_aux.IC_ESPANOL)
            puntuacion = chi2 + ic_normalizado * 1000
            
            if puntuacion < mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_letra = chr(shift + ord('A'))
                mejor_ic = ic
        
        clave.append(mejor_letra)
    
    clave_str = ""

    for caracter in clave:
            clave_str += caracter    

    return clave_str
