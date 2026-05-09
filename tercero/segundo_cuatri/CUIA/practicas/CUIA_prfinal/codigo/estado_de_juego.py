def crear_tropa(id, tipo_tropa, tropas):
    #dragon fuego
    if tipo_tropa == 0:
        tropas[id][0] = 650
        tropas[id][1] = 250
        tropas[id][2] = 100 #hace 100 de daño a cada tropa enemiga
        tropas[id][3] = tipo_tropa
    #dragon agua
    if tipo_tropa == 1:
        tropas[id][0] = 850
        tropas[id][1] = 200
        tropas[id][2] = 50  # cura 50 de vida a cada tropa aliada
        tropas[id][3] = tipo_tropa
    #golem
    if tipo_tropa == 2:
        tropas[id][0] = 1000
        tropas[id][1] = 150
        tropas[id][2] = 0.8 # reduce el daño recibido a las tropas aliadas en un 20%
        tropas[id][3] = tipo_tropa
    #erizo
    if tipo_tropa == 3:
        tropas[id][0] = 500
        tropas[id][1] = 200
        tropas[id][2] = 200 #realiza 200 de daño a la tropa que le ha atacado
        tropas[id][3] = tipo_tropa  
    #curandero
    if tipo_tropa == 4:
        tropas[id][0] = 450
        tropas[id][1] = 100
        tropas[id][2] = 150 #cura a las tropas aliadas cada vez que transcurre un turno como atacante 
        tropas[id][3] = tipo_tropa
    #gargola
    if tipo_tropa == 5:
        tropas[id][0] = 500
        tropas[id][1] = 150
        tropas[id][2] = 300 #si la tropa a la que ataca tiene menos de 300 de vida la mata de golpe
        tropas[id][3] = tipo_tropa
    #monstruo chicle
    if tipo_tropa == 6:
        tropas[id][0] = 800
        tropas[id][1] = 150
        tropas[id][2] = 0.9 #cuando recibe daño reduce el daño de la tropa en un 10%(solo para ataques basicos)
        tropas[id][3] = tipo_tropa
    #serpiente
    if tipo_tropa == 7:
        tropas[id][0] = 300
        tropas[id][1] = 200
        tropas[id][2] = 0 #si esta como primera tropa y ya ha atacado antes mata de un golpe, una vez ataca resetea
        tropas[id][3] = tipo_tropa

def tropa_con_vida(id, tropas):
    if tropas[id][0] > 0:
        return True
    else:
        return False
    
def atacar(id, tropa_delantera_ataque, tropa_delantera_defensa, jugador_activo, tropas):
    if jugador_activo == 1:
        jugador_defensor = 2
    else:
        jugador_defensor = 1

    if id == tropa_delantera_ataque :
        defensa_extra = 1
        
        #habilidad golem
        if jugador_activo == 2:
            if tropa_con_vida(0, tropas) and tropas[0][3] == 2:
                defensa_extra = tropas[0][2]
            elif tropa_con_vida(1, tropas) and tropas[1][3] == 2:
                defensa_extra = tropas[1][2]
        else:
            if tropa_con_vida(2, tropas) and tropas[2][3] == 2:
                defensa_extra = tropas[2][2]
            elif tropa_con_vida(3, tropas) and tropas[3][3] == 2:
                defensa_extra = tropas[3][2]

        # habilidad erizo
        if tropas[tropa_delantera_defensa][3] == 3:
            daño_recibido = tropas[tropa_delantera_defensa][2]
        else:
            daño_recibido = 0
        
        if tropa_con_vida(tropa_delantera_defensa, tropas):
            tropas[tropa_delantera_defensa][0] -= tropas[id][1] * defensa_extra
        else:
            pass 

        if tropas[id][3] == 0: # Dragon Fuego
            if jugador_activo == 1:
                if tropa_con_vida(2, tropas):
                    tropas[2][0] -= tropas[id][2] * defensa_extra
                if tropa_con_vida(3, tropas):
                    tropas[3][0] -= tropas[id][2] * defensa_extra
            else:
                if tropa_con_vida(0, tropas):
                    tropas[0][0] -= tropas[id][2] * defensa_extra
                if tropa_con_vida(1, tropas):
                    tropas[1][0] -= tropas[id][2] * defensa_extra
            
            tropas[id][0] -= daño_recibido

        if tropas[id][3] == 1: # Dragon Agua
            if jugador_activo == 1:
                if tropa_con_vida(0, tropas):
                    tropas[0][0] += tropas[id][2]
                if tropa_con_vida(1, tropas):
                    tropas[1][0] += tropas[id][2]
            else: 
                if tropa_con_vida(2, tropas):
                    tropas[2][0] += tropas[id][2]
                if tropa_con_vida(3, tropas):
                    tropas[3][0] += tropas[id][2]

            tropas[id][0] -= daño_recibido

        if tropas[id][3] == 2: # Golem
            tropas[id][0] -= daño_recibido

        if tropas[id][3] == 3: # Erizo
            tropas[id][0] -= daño_recibido

        if tropas[id][3] == 4: # Curandero
            tropas[id][0] -= daño_recibido
        
        if tropas[id][3] == 5: # Gargola
            if tropa_con_vida(tropa_delantera_defensa, tropas) and tropas[tropa_delantera_defensa][0] <= tropas[id][2]:
                tropas[tropa_delantera_defensa][0] = 0

            tropas[id][0] -= daño_recibido

        if tropas[id][3] == 7: # Serpìente
            if tropas[id][2] == 1:
                if tropa_con_vida(tropa_delantera_defensa, tropas) and tropas[tropa_delantera_defensa][0] <= tropas[id][2]:
                    tropas[tropa_delantera_defensa][0] = 0
                    tropas[id][2] = 0
            else:
                tropas[id][2] = 1
            tropas[id][0] -= daño_recibido

        #habilidad curandero
        if jugador_activo == 1:
            if tropa_con_vida(0, tropas) and tropas[0][3] == 4:
                tropas[0][0] += tropas[0][2]
                if tropa_con_vida(1, tropas):
                    tropas[1][0] += tropas[0][2]
            if tropa_con_vida(1, tropas) and tropas[1][3] == 4:
                tropas[1][0] += tropas[1][2]
                if tropa_con_vida(0, tropas):
                    tropas[0][0] += tropas[1][2]
        else: 
            if tropa_con_vida(2, tropas) and tropas[2][3] == 4:
                tropas[2][0] += tropas[2][2]
                if tropa_con_vida(3, tropas):
                    tropas[3][0] += tropas[2][2]
            if tropa_con_vida(3, tropas) and tropas[3][3] == 4:
                tropas[3][0] += tropas[3][2]
                if tropa_con_vida(2, tropas):
                    tropas[2][0] += tropas[3][2]

        #habilidad monstruo de chicle
        if tropas[tropa_delantera_defensa][3] == 6:
            tropas[id][1] *= tropas[tropa_delantera_defensa][2]

    else:
        defensa_extra = 1
        #habilidad golem
        if jugador_activo == 2:
            if tropa_con_vida(0, tropas) and tropas[0][3] == 2:
                defensa_extra = tropas[0][2]
            elif tropa_con_vida(1, tropas) and tropas[1][3] == 2:
                defensa_extra = tropas[1][2]
        else: 
            if tropa_con_vida(2, tropas) and tropas[2][3] == 2:
                defensa_extra = tropas[2][2]
            elif tropa_con_vida(3, tropas) and tropas[3][3] == 2:
                defensa_extra = tropas[3][2]

        #habilidad erizo
        if tropas[tropa_delantera_defensa][3] == 3:
            daño_recibido = tropas[tropa_delantera_defensa][2]
        else:
            daño_recibido = 0

        #habilidad curandero
        if jugador_activo == 1:
            if tropa_con_vida(0, tropas) and tropas[0][3] == 4:
                tropas[0][0] += tropas[0][2]
                if tropa_con_vida(1, tropas):
                    tropas[1][0] += tropas[0][2]
            if tropa_con_vida(1, tropas) and tropas[1][3] == 4:
                tropas[1][0] += tropas[1][2]
                if tropa_con_vida(0, tropas):
                    tropas[0][0] += tropas[1][2]
        else: 
            if tropa_con_vida(2, tropas) and tropas[2][3] == 4:
                tropas[2][0] += tropas[2][2]
                if tropa_con_vida(3, tropas):
                    tropas[3][0] += tropas[2][2]
            if tropa_con_vida(3, tropas) and tropas[3][3] == 4:
                tropas[3][0] += tropas[3][2]
                if tropa_con_vida(2, tropas):
                    tropas[2][0] += tropas[3][2]
        
        if tropa_con_vida(tropa_delantera_defensa, tropas):
            tropas[tropa_delantera_defensa][0] -= tropas[id][1] * defensa_extra
        else:
            pass

        tropas[id][0] -= daño_recibido

        #habilidad monstruo de chicle
        if tropas[tropa_delantera_defensa][3] == 6:
            tropas[id][1] *= tropas[tropa_delantera_defensa][2]

    return tropas

def cambiar_tropa_delantera(tropa_delantera, id_jugador, tropas):
    if tropa_con_vida(tropa_delantera, tropas):
        if id_jugador == 1:
            if tropa_delantera == 0:
                if tropa_con_vida(1, tropas):
                    return 1
                else:
                    return 0
            elif tropa_delantera == 1:
                if tropa_con_vida(0, tropas):
                    return 0
                else:
                    return 1
        elif id_jugador == 2:
            if tropa_delantera == 2:
                if tropa_con_vida(3, tropas):
                    return 3
                else:
                    return 2
            elif tropa_delantera == 3:
                if tropa_con_vida(2, tropas):
                    return 2
                else:
                    return 3
    else:
        if id_jugador == 1:
            if tropa_con_vida(0, tropas):
                return 0
            elif tropa_con_vida(1, tropas):
                return 1
            else:
                return None
        elif id_jugador == 2:
            if tropa_con_vida(2, tropas):
                return 2
            elif tropa_con_vida(3, tropas):
                return 3
            else:
                return None
    return tropa_delantera

def jugador_sin_tropas(id_jugador, tropas):
    if id_jugador == 1:
        return not tropa_con_vida(0, tropas) and not tropa_con_vida(1, tropas)
    elif id_jugador == 2:
        return not tropa_con_vida(2, tropas) and not tropa_con_vida(3, tropas)
    return False
