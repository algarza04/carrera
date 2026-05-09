import cv2
import numpy as np
import cuia
import speech_recognition as sr
import estado_de_juego
import sys
import reconocimiento_facial

# Variables globales
id_jugador = 1
marcadores_seleccionados = 0
tropas = np.empty((4, 4))
tropa_delantera1 = 0
tropa_delantera2 = 2
exit_flag = False
salir = False
perdedor = [False, False]

modelos = {
    0: cuia.modeloGLTF('modelos/vacio.glb'),
    1: cuia.modeloGLTF('modelos/vacio.glb'),
    2: cuia.modeloGLTF('modelos/vacio.glb'),
    3: cuia.modeloGLTF('modelos/vacio.glb'),
}

usuario = reconocimiento_facial.reconocer_o_registrar()

def rotar_2y3(modelos, marcadores_seleccionados):
    if marcadores_seleccionados == 2 or marcadores_seleccionados == 3:
        modelos[marcadores_seleccionados].rotar((0, 0, np.pi / 1.0))

# --- VOZ ---
def voz_callback(recognizer, audio):
    global exit_flag, id_jugador, marcadores_seleccionados, modelos, salir, tropa_delantera1, tropa_delantera2, perdedor, tropas, usuario

    try:
        texto = recognizer.recognize_google(audio, language=usuario["idioma"]).lower()
        
        if usuario["idioma"] == "es-ES":
            print("Dijiste:", texto)
        else:
            print("You said:", texto)

        if not salir:
            if usuario["idioma"] == "es-ES":
                if "cambiar idioma a inglés" in texto:
                    reconocimiento_facial.guardar_idioma(usuario["id"], "en-US")
                    usuarios_data = reconocimiento_facial.cargar_usuarios()
                    for u_id in usuarios_data["ids"]:
                        if u_id == usuario["id"]:
                            usuario["idioma"] = usuarios_data["idiomas"].get(str(u_id), "es-ES")
                            break
                    print("Idioma cambiado a Inglés.")
                    return
                elif "cargar lista de favoritos" in texto:
                    if usuario and "favoritas" in usuario:
                        for i,carta in enumerate(usuario["favoritas"]):
                            if i >= 4: break
                            elif carta == "dragon_fuego": nuevo_modelo = cuia.modeloGLTF('modelos/dragon_fuego.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 0, tropas); rotar_2y3(modelos, i)
                            elif carta == "dragon_agua": nuevo_modelo = cuia.modeloGLTF('modelos/dragon_agua.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 1, tropas); rotar_2y3(modelos, i)
                            elif carta == "golem": nuevo_modelo = cuia.modeloGLTF('modelos/golem.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 2, tropas); rotar_2y3(modelos, i)
                            elif carta == "erizo": nuevo_modelo = cuia.modeloGLTF('modelos/erizo.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 3, tropas); rotar_2y3(modelos, i)
                            elif carta == "curandero": nuevo_modelo = cuia.modeloGLTF('modelos/curandero.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 4, tropas); rotar_2y3(modelos, i)
                            elif carta == "gargola": nuevo_modelo = cuia.modeloGLTF('modelos/gargola.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 5, tropas); rotar_2y3(modelos, i)
                            elif carta == "monstruo_chicle": nuevo_modelo = cuia.modeloGLTF('modelos/monstruo_chicle.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 6, tropas); rotar_2y3(modelos, i)
                            elif carta == "serpiente": nuevo_modelo = cuia.modeloGLTF('modelos/serpiente.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 7, tropas); rotar_2y3(modelos, i)
                        marcadores_seleccionados = len(usuario["favoritas"])
                        if marcadores_seleccionados >= 4: salir = True
                        print("Favoritas cargadas.")
                    else:
                        print("No hay favoritas guardadas para este usuario.")
                    return
                elif "modificar lista de favoritos" in texto:
                    nuevas_favoritas = []
                    print("Dime las cartas que quieres guardar como favoritas (máximo 4). Di 'fin' para terminar antes de tiempo.")
                    with sr.Microphone() as source:
                        while len(nuevas_favoritas) < 4:
                            try:
                                print("Escuchando carta...")
                                audio = recognizer.listen(source, timeout=5)
                                carta = recognizer.recognize_google(audio, language=usuario["idioma"]).lower()
                                print(f"Detectado: {carta}")

                                if "fin" in carta: break
                                elif "dragón de fuego" in carta: nuevas_favoritas.append("dragon_fuego")
                                elif "dragón de agua" in carta: nuevas_favoritas.append("dragon_agua")
                                elif "golem" in carta: nuevas_favoritas.append("golem")
                                elif "erizo" in carta: nuevas_favoritas.append("erizo")
                                elif "curandero" in carta: nuevas_favoritas.append("curandero")
                                elif "gárgola" in carta: nuevas_favoritas.append("gargola")
                                elif "monstruo de chicle" in carta: nuevas_favoritas.append("monstruo_chicle")
                                elif "serpiente" in carta: nuevas_favoritas.append("serpiente")
                                else: print("Carta no reconocida.")
                            except sr.UnknownValueError:
                                print("No entendí. Repite por favor.")
                            except sr.WaitTimeoutError:
                                print("No se detectó voz. Intenta de nuevo.")
                    if nuevas_favoritas:
                        reconocimiento_facial.guardar_favorito(usuario["id"], nuevas_favoritas)
                        usuarios_data = reconocimiento_facial.cargar_usuarios()
                        for i, id_u in enumerate(usuarios_data["ids"]):
                            if id_u == usuario["id"]:
                                usuario = {"id": id_u, "nombre": usuarios_data["nombres"][i], "favoritas": usuarios_data["favoritos"].get(str(id_u), []), "idioma": usuarios_data["idiomas"].get(str(id_u), "es-ES")}
                                break
                        print(f"Lista de favoritas actualizada: {usuario['favoritas']}")
                    else: print("No se añadió ninguna carta.")
                    return
                # Añadir tropas (Spanish)
                elif "añadir dragón de fuego" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/dragon_fuego.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 0, tropas); rotar_2y3(modelos, marcadores_seleccionados);marcadores_seleccionados += 1; print("Se añadió un Dragón de Fuego.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir dragón de agua" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/dragon_agua.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 1, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió un Dragón de Agua.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir golem" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/golem.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 2, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió un Gólem.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir erizo" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/erizo.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 3, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió un Erizo.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir curandero" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/curandero.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 4, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió un Curandero.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir gárgola" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/gargola.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 5, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió una Gárgola.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir monstruo de chicle" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/monstruo_chicle.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 6, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió un Monstruo de Chicle.")
                    else: print("Ya hay 4 tropas.")
                elif "añadir serpiente" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/serpiente.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 7, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Se añadió una Serpiente.")
                    else: print("Ya hay 4 tropas.")
                else:
                    print("Comando no válido o no permitido en esta fase.")
            
            elif usuario["idioma"] == "en-US":
                if "change language to spanish" in texto:
                    reconocimiento_facial.guardar_idioma(usuario["id"], "es-ES")
                    usuarios_data = reconocimiento_facial.cargar_usuarios()
                    for u_id in usuarios_data["ids"]:
                        if u_id == usuario["id"]:
                            usuario["idioma"] = usuarios_data["idiomas"].get(str(u_id), "es-ES")
                            break
                    print("Language changed to Spanish.")
                    return
                elif "load favorites list" in texto:
                    if usuario and "favoritas" in usuario:
                        for i,carta in enumerate(usuario["favoritas"]):
                            if i >= 4: break
                            elif carta == "dragon_fuego": nuevo_modelo = cuia.modeloGLTF('modelos/dragon_fuego.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 0, tropas); rotar_2y3(modelos, i)
                            elif carta == "dragon_agua": nuevo_modelo = cuia.modeloGLTF('modelos/dragon_agua.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 1, tropas); rotar_2y3(modelos, i)
                            elif carta == "golem": nuevo_modelo = cuia.modeloGLTF('modelos/golem.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 2, tropas); rotar_2y3(modelos, i)
                            elif carta == "erizo": nuevo_modelo = cuia.modeloGLTF('modelos/erizo.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 3, tropas); rotar_2y3(modelos, i)
                            elif carta == "curandero": nuevo_modelo = cuia.modeloGLTF('modelos/curandero.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 4, tropas); rotar_2y3(modelos, i)
                            elif carta == "gargola": nuevo_modelo = cuia.modeloGLTF('modelos/gargola.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 5, tropas); rotar_2y3(modelos, i)
                            elif carta == "monstruo_chicle": nuevo_modelo = cuia.modeloGLTF('modelos/monstruo_chicle.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 6, tropas);rotar_2y3(modelos, i)
                            elif carta == "serpiente": nuevo_modelo = cuia.modeloGLTF('modelos/serpiente.glb'); actualizar_modelo(i, nuevo_modelo); estado_de_juego.crear_tropa(i, 7, tropas);rotar_2y3(modelos, i)
                        marcadores_seleccionados = len(usuario["favoritas"])
                        if marcadores_seleccionados >= 4: salir = True
                        print("Favorites loaded.")
                    else:
                        print("No favorites saved for this user.")
                    return
                elif "modify favorites list" in texto:
                    nuevas_favoritas = []
                    print("Tell me the cards you want to save as favorites (maximum 4). Say 'finish' to end early.")
                    with sr.Microphone() as source:
                        while len(nuevas_favoritas) < 4:
                            try:
                                print("Listening for card...")
                                audio = recognizer.listen(source, timeout=5)
                                carta = recognizer.recognize_google(audio, language=usuario["idioma"]).lower()
                                print(f"Detected: {carta}")

                                if "finish" in carta: break
                                elif "fire dragon" in carta: nuevas_favoritas.append("dragon_fuego")
                                elif "water dragon" in carta: nuevas_favoritas.append("dragon_agua")
                                elif "golem" in carta: nuevas_favoritas.append("golem")
                                elif "hedgehog" in carta: nuevas_favoritas.append("erizo")
                                elif "healer" in carta: nuevas_favoritas.append("curandero")
                                elif "gargoyle" in carta: nuevas_favoritas.append("gargola")
                                elif "bubblegum monster" in carta: nuevas_favoritas.append("monstruo_chicle")
                                elif "snake" in carta: nuevas_favoritas.append("serpiente")
                                else: print("Card not recognized.")
                            except sr.UnknownValueError:
                                print("I didn't understand. Please repeat.")
                            except sr.WaitTimeoutError:
                                print("No speech detected. Try again.")
                    if nuevas_favoritas:
                        reconocimiento_facial.guardar_favorito(usuario["id"], nuevas_favoritas)
                        usuarios_data = reconocimiento_facial.cargar_usuarios()
                        for i, id_u in enumerate(usuarios_data["ids"]):
                            if id_u == usuario["id"]:
                                usuario = {"id": id_u, "nombre": usuarios_data["nombres"][i], "favoritas": usuarios_data["favoritos"].get(str(id_u), []), "idioma": usuarios_data["idiomas"].get(str(id_u), "es-ES")}
                                break
                        print(f"Favorites list updated: {usuario['favoritas']}")
                    else: print("No cards were added.")
                    return
                # Añadir tropas (English)
                elif "add fire dragon" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/dragon_fuego.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 0, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Fire Dragon.")
                    else: print("Already have 4 troops.")
                elif "add water dragon" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/dragon_agua.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 1, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Water Dragon.")
                    else: print("Already have 4 troops.")
                elif "add golem" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/golem.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 2, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Golem.")
                    else: print("Already have 4 troops.")
                elif "add hedgehog" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/erizo.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 3, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Hedgehog.")
                    else: print("Already have 4 troops.")
                elif "add healer" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/curandero.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 4, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Healer.")
                    else: print("Already have 4 troops.")
                elif "add gargoyle" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/gargola.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 5, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Gargoyle.")
                    else: print("Already have 4 troops.")
                elif "add bubblegum monster" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/monstruo_chicle.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 6, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Bubblegum Monster.")
                    else: print("Already have 4 troops.")
                elif "add snake" in texto:
                    if marcadores_seleccionados < 4: nuevo_modelo = cuia.modeloGLTF('modelos/serpiente.glb'); actualizar_modelo(marcadores_seleccionados, nuevo_modelo); estado_de_juego.crear_tropa(marcadores_seleccionados, 7, tropas); rotar_2y3(modelos, marcadores_seleccionados); marcadores_seleccionados += 1; print("Added a Snake.")
                    else: print("Already have 4 troops.")
                else:
                    print("Invalid command or not allowed in this phase.")
            
            else:
                if "cambiar idioma a inglés" in texto:
                    reconocimiento_facial.guardar_idioma(usuario["id"], "en-US")
                    usuarios_data = reconocimiento_facial.cargar_usuarios()
                    for u_id in usuarios_data["ids"]:
                        if u_id == usuario["id"]:
                            usuario["idioma"] = usuarios_data["idiomas"].get(str(u_id), "es-ES")
                            break
                    print("Language changed to English.")
                    return
                elif "cambiar idioma a español" in texto:
                    reconocimiento_facial.guardar_idioma(usuario["id"], "es-ES")
                    usuarios_data = reconocimiento_facial.cargar_usuarios()
                    for u_id in usuarios_data["ids"]:
                        if u_id == usuario["id"]:
                            usuario["idioma"] = usuarios_data["idiomas"].get(str(u_id), "es-ES")
                            break
                    print("Idioma cambiado a Español.")
                    return
                print("Command not recognized. Please switch to a supported language (English or Spanish).")
            
            # una vez estan las tropas elegidas pasamos a la fase de ataques
            if marcadores_seleccionados < 4:
                if usuario["idioma"] == "es-ES":
                    print(f"Marcadores seleccionados: {marcadores_seleccionados}/4")
                else:
                    print(f"Markers selected: {marcadores_seleccionados}/4")

            if marcadores_seleccionados >= 4 and not salir: # Check not 'salir' to avoid re-printing
                salir = True
                if usuario["idioma"] == "es-ES":
                    print("Tropas completas. Comienza la batalla.")
                else:
                    print("Troops complete. Battle begins.")
            return

        # ETAPA 2: Una vez están los marcadores seleccionados comienza la batalla
        tropa_trasera1 = 1 if tropa_delantera1 == 0 else 0
        tropa_trasera2 = 3 if tropa_delantera2 == 2 else 2

        # Si la tropa delantera muere se cambia por la otra
        if not estado_de_juego.tropa_con_vida(tropa_delantera1, tropas):
            tropa_delantera1 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera1, 1, tropas)
        if not estado_de_juego.tropa_con_vida(tropa_delantera2, tropas):
            tropa_delantera2 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera2, 2, tropas)

        perdedor[0] = estado_de_juego.jugador_sin_tropas(1, tropas)
        perdedor[1] = estado_de_juego.jugador_sin_tropas(2, tropas)

        if perdedor[0] or perdedor[1]:
            if perdedor[0]:
                if usuario["idioma"] == "es-ES":
                    print("¡El Jugador 1 ha perdido! ¡El Jugador 2 gana!")
                else:
                    print("Player 1 has lost! Player 2 wins!")
                exit_flag = True
            elif perdedor[1]:
                if usuario["idioma"] == "es-ES":
                    print("¡El Jugador 2 ha perdido! ¡El Jugador 1 gana!")
                else:
                    print("Player 2 has lost! Player 1 wins!")
                exit_flag = True
            sys.exit() # FIN

        # Proceso de los combates
        if usuario["idioma"] == "es-ES":
            if "cambiar tropa delantera" in texto:
                if id_jugador == 1:
                    tropa_antes_cambio = tropa_delantera1
                    tropa_delantera1 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera1, id_jugador, tropas)
                    if tropa_delantera1 is None:
                        print("¡No te quedan tropas para cambiar!")
                    elif tropa_antes_cambio != tropa_delantera1:
                        print(f"Jugador 1 cambió la tropa delantera a {tropa_delantera1}.")
                        id_jugador = 2
                    else:
                        print("No se pudo cambiar la tropa delantera (la otra tropa podría estar sin vida o ya es la delantera).")
                else: # id_jugador == 2
                    tropa_antes_cambio = tropa_delantera2
                    tropa_delantera2 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera2, id_jugador, tropas)
                    if tropa_delantera2 is None:
                        print("¡No te quedan tropas para cambiar!")
                    elif tropa_antes_cambio != tropa_delantera2:
                        print(f"Jugador 2 cambió la tropa delantera a {tropa_delantera2}.")
                        id_jugador = 1
                    else:
                        print("No se pudo cambiar la tropa delantera (la otra tropa podría estar sin vida o ya es la delantera).")
            elif "atacar con la primera tropa" in texto:
                if id_jugador == 1:
                    if estado_de_juego.tropa_con_vida(tropa_delantera1, tropas):
                        print(f"Jugador 1 ataca con su tropa delantera (ID: {tropa_delantera1}).")
                        estado_de_juego.atacar(tropa_delantera1, tropa_delantera1, tropa_delantera2, id_jugador, tropas)
                        id_jugador = 2
                    else:
                        print("No se puede atacar con la tropa delantera porque no tiene vida.")
                else: # id_jugador == 2
                    if estado_de_juego.tropa_con_vida(tropa_delantera2, tropas):
                        print(f"Jugador 2 ataca con su tropa delantera (ID: {tropa_delantera2}).")
                        estado_de_juego.atacar(tropa_delantera2, tropa_delantera2, tropa_delantera1, id_jugador, tropas)
                        id_jugador = 1
                    else:
                        print("No se puede atacar con la tropa delantera porque no tiene vida.")
            elif "atacar con la segunda tropa" in texto:
                if id_jugador == 1:
                    if estado_de_juego.tropa_con_vida(tropa_trasera1, tropas):
                        print(f"Jugador 1 ataca con su tropa trasera (ID: {tropa_trasera1}).")
                        estado_de_juego.atacar(tropa_trasera1, tropa_delantera1, tropa_delantera2, id_jugador, tropas)
                        id_jugador = 2
                    else:
                        print("No se puede atacar con la tropa trasera porque no tiene vida.")
                else: # id_jugador == 2
                    if estado_de_juego.tropa_con_vida(tropa_trasera2, tropas):
                        print(f"Jugador 2 ataca con su tropa trasera (ID: {tropa_trasera2}).")
                        estado_de_juego.atacar(tropa_trasera2, tropa_delantera2, tropa_delantera1, id_jugador, tropas)
                        id_jugador = 1
                    else:
                        print("No se puede atacar con la tropa trasera porque no tiene vida.")
            elif "me rindo" in texto:
                if id_jugador == 1:
                    perdedor[0] = True
                    exit_flag = True
                    print("El Jugador 1 se ha rendido. ¡El Jugador 2 gana!")
                else: # id_jugador == 2
                    perdedor[1] = True
                    print("El Jugador 2 se ha rendido. ¡El Jugador 1 gana!")
                    exit_flag = True
                sys.exit()
            else: 
                print("Comando no reconocido. Intenta 'atacar con la primera tropa', 'atacar con la segunda tropa', 'cambiar tropa delantera', o 'me rindo'.")

        elif usuario["idioma"] == "en-US":
            if "change front troop" in texto:
                if id_jugador == 1:
                    tropa_antes_cambio = tropa_delantera1
                    tropa_delantera1 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera1, id_jugador, tropas)
                    if tropa_delantera1 is None:
                        print("You have no more troops to swap!")
                    elif tropa_antes_cambio != tropa_delantera1:
                        print(f"Player 1 changed the front troop to {tropa_delantera1}.")
                        id_jugador = 2
                    else:
                        print("Could not change front troop (the other troop might be out of life or is already the front one).")
                else: # id_jugador == 2
                    tropa_antes_cambio = tropa_delantera2
                    tropa_delantera2 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera2, id_jugador, tropas)
                    if tropa_delantera2 is None:
                        print("You have no more troops to swap!")
                    elif tropa_antes_cambio != tropa_delantera2:
                        print(f"Player 2 changed the front troop to {tropa_delantera2}.")
                        id_jugador = 1
                    else:
                        print("Could not change front troop (the other troop might be out of life or is already the front one).")
            elif "attack with first troop" in texto:
                if id_jugador == 1:
                    if estado_de_juego.tropa_con_vida(tropa_delantera1, tropas):
                        print(f"Player 1 attacks with their front troop (ID: {tropa_delantera1}).")
                        estado_de_juego.atacar(tropa_delantera1, tropa_delantera1, tropa_delantera2, id_jugador, tropas)
                        id_jugador = 2
                    else:
                        print("Cannot attack with the front troop because it has no life.")
                else: # id_jugador == 2
                    if estado_de_juego.tropa_con_vida(tropa_delantera2, tropas):
                        print(f"Player 2 attacks with their front troop (ID: {tropa_delantera2}).")
                        estado_de_juego.atacar(tropa_delantera2, tropa_delantera2, tropa_delantera1, id_jugador, tropas)
                        id_jugador = 1
                    else:
                        print("Cannot attack with the front troop because it has no life.")
            elif "attack with second troop" in texto:
                if id_jugador == 1:
                    if estado_de_juego.tropa_con_vida(tropa_trasera1, tropas):
                        print(f"Player 1 attacks with their rear troop (ID: {tropa_trasera1}).")
                        estado_de_juego.atacar(tropa_trasera1, tropa_delantera1, tropa_delantera2, id_jugador, tropas)
                        id_jugador = 2
                    else:
                        print("Cannot attack with the rear troop because it has no life.")
                else: # id_jugador == 2
                    if estado_de_juego.tropa_con_vida(tropa_trasera2, tropas):
                        print(f"Player 2 attacks with their rear troop (ID: {tropa_trasera2}).")
                        estado_de_juego.atacar(tropa_trasera2, tropa_delantera2, tropa_delantera1, id_jugador, tropas)
                        id_jugador = 1
                    else:
                        print("Cannot attack with the rear troop because it has no life.")
            elif "i surrender" in texto:
                if id_jugador == 1:
                    perdedor[0] = True
                    exit_flag = True
                    print("Player 1 has surrendered. Player 2 wins!")
                else: # id_jugador == 2
                    perdedor[1] = True
                    print("Player 2 has surrendered. Player 1 wins!")
                    exit_flag = True
                sys.exit()
            else: # Unrecognized command in English
                print("Command not recognized. Try 'attack with first troop', 'attack with second troop', 'change front troop', or 'i surrender'.")
        else:
            print("Command not recognized. Please switch to a supported language (English or Spanish).")

    except sr.UnknownValueError:
        if usuario["idioma"] == "es-ES":
            print("No pude entender el audio.")
        else:
            print("I didn't understand the audio.")
    except sr.RequestError as e:
        if usuario["idioma"] == "es-ES":
            print(f"Error en el servicio de reconocimiento de voz; {e}")
        else:
            print(f"Speech recognition service error; {e}")
   
# Escucha en segundo plano
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)
    print("Micrófono calibrado. Escuchando...")
stop_listening = r.listen_in_background(m, voz_callback)

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
detector = cv2.aruco.ArucoDetector(diccionario)

def actualizar_modelo(i, nuevo_modelo):
    global escena, modelos
    # Reemplazar en el diccionario
    modelos[i] = nuevo_modelo
    # Configurar modelo nuevo
    modelos[i].rotar((np.pi / 2.0, 0, 0))
    modelos[i].escalar(0.2)
    modelos[i].flotar()
    animaciones = modelos[i].animaciones()
    if animaciones:
        modelos[i].animar(animaciones[0])
    # Agregar a la escena
    escena.agregar_modelo(modelos[i])
    escena.ilumina_modelo(modelos[i])

cam = 0
bk = cuia.bestBackend(cam)
webcam = cv2.VideoCapture(cam, bk)
ancho = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
webcam.release()

# Calibración
try:
    import camara
    cameraMatrix = camara.cameraMatrix
    distCoeffs = camara.distCoeffs
except ImportError:
    cameraMatrix = np.array([
        [1000, 0, ancho / 2],
        [0, 1000, alto / 2],
        [0, 0, 1]
    ])
    distCoeffs = np.zeros((5, 1))

# Configuramos los modelos
for modelo in modelos.values():
    modelo.rotar((np.pi / 2.0, 0, 0))
    modelo.escalar(0.2)
    modelo.flotar()
    animaciones = modelo.animaciones()
    if animaciones:
        modelo.animar(animaciones[0])

# Funciones auxiliares
def fromOpencvToPygfx(rvec, tvec):
    pose = np.eye(4)
    rot_matrix, _ = cv2.Rodrigues(rvec)
    pose[:3, :3] = rot_matrix
    pose[:3, 3] = tvec.flatten()
    pose[1:3, :] *= -1  # Ajuste de ejes Y y Z
    return np.linalg.inv(pose)  # IMPORTANTE

def fov(cameraMatrix, ancho, alto):
    if ancho > alto:
        f = cameraMatrix[1, 1]
        fov_rad = 2 * np.arctan(alto / (2 * f))
    else:
        f = cameraMatrix[0, 0]
        fov_rad = 2 * np.arctan(ancho / (2 * f))
    return np.rad2deg(fov_rad)

# Crear escena PYGFX
escena = cuia.escenaPYGFX(fov(cameraMatrix, ancho, alto), ancho, alto)
for modelo in modelos.values():
    escena.agregar_modelo(modelo)
    escena.ilumina_modelo(modelo)
escena.iluminar()

ar = cuia.myVideo(cam, bk)

# Preparar el detector ArUco
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
detector = cv2.aruco.ArucoDetector(diccionario)

def relative_pose(rvec1, tvec1, rvec2, tvec2):
    R1, _ = cv2.Rodrigues(rvec1)
    R2, _ = cv2.Rodrigues(rvec2)

    T1 = np.eye(4)
    T1[:3, :3] = R1
    T1[:3, 3] = tvec1.flatten()

    T2 = np.eye(4)
    T2[:3, :3] = R2
    T2[:3, 3] = tvec2.flatten()

    T_rel = np.linalg.inv(T1) @ T2
    return T_rel

def quitar_tildes(texto):
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'ñ': 'n',
        'Ñ': 'N'
    }
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    return texto

# Función de renderizado en realidad mixta
def realidadMixta(frame):
    bboxs, ids, _ = detector.detectMarkers(frame)
    modelos_visibles = set()

    if ids is not None and len(bboxs) > 0:
        tam = 0.10
        objPoints = np.array([
            [-tam/2.0,  tam/2.0, 0.0],
            [ tam/2.0,  tam/2.0, 0.0],
            [ tam/2.0, -tam/2.0, 0.0],
            [-tam/2.0, -tam/2.0, 0.0]
        ])

        poses_detectadas = {}
        for i, id_marker in enumerate(ids.flatten()):
            ret, rvec, tvec = cv2.solvePnP(objPoints, bboxs[i], cameraMatrix, distCoeffs)
            if ret:
                poses_detectadas[id_marker] = (rvec, tvec)

        if not poses_detectadas:
            return frame

        id_ref = min(poses_detectadas.keys())
        rvec_ref, tvec_ref = poses_detectadas[id_ref]
        escena.actualizar_camara(fromOpencvToPygfx(rvec_ref, tvec_ref))

        for id_modelo, modelo in modelos.items():
            if id_modelo in poses_detectadas:
                rvec_modelo, tvec_modelo = poses_detectadas[id_modelo]

                T_rel = relative_pose(rvec_ref, tvec_ref, rvec_modelo, tvec_modelo)
                t_rel = T_rel[:3, 3]

                modelo.trasladar(t_rel)
                modelo.escalar(0.2)

                modelos_visibles.add(id_modelo)
            else:
                modelo.escalar(0)

    else:
        for modelo in modelos.values():
            modelo.escalar(0)

    imagen_render = escena.render()
    imagen_render_bgra = cv2.cvtColor(imagen_render, cv2.COLOR_RGBA2BGRA)
    resultado = cuia.alphaBlending(imagen_render_bgra, frame)

    # Texto flotante con vida/daño/muerta sobre cada modelo
    if salir:
        if ids is not None and len(bboxs) > 0:
            for id_marker in ids.flatten():
                if id_marker in poses_detectadas:
                    rvec, tvec = poses_detectadas[id_marker]
                    posicion_3D_texto = np.array([[0, 0, -0.05]])
                    punto_2D, _ = cv2.projectPoints(posicion_3D_texto, rvec, tvec, cameraMatrix, distCoeffs)
                    x, y = punto_2D[0][0].astype(int)

                    vida = tropas[id_marker][0]
                    daño = tropas[id_marker][1]
                    if vida > 0:
                        texto = f"{int(vida)} HP, {int(daño)} AT"
                        color = (255, 255, 0)  # amarillo
                    else:
                        if usuario["idioma"] == "es-ES":
                            texto = "MUERTA"
                        else:   
                            texto = "DEAD"
                        color = (0, 0, 255)  # rojo

                cv2.putText(resultado, texto, (x - 30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)

    # Información general en pantalla
    if not salir:
        nombre_sin_tildes = quitar_tildes(usuario['nombre'])
        if usuario["idioma"] == "es-ES":
            cv2.putText(resultado, f"Bienvenido {nombre_sin_tildes}, id: {usuario['id']}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
        elif usuario["idioma"] == "en-US":
            cv2.putText(resultado, f"Welcome {nombre_sin_tildes}, id: {usuario['id']}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
        else:
            cv2.putText(resultado, f"Welcome {nombre_sin_tildes}, id: {usuario['id']}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
    else:
        if perdedor[0] and perdedor[1]:
            if usuario["idioma"] == "es-ES":
                cv2.putText(resultado, f"Ha habido un empate", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            elif usuario["idioma"] == "en-US":
                cv2.putText(resultado, f"It's a tie", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            else:
                cv2.putText(resultado, f"It's a tie", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
        elif perdedor[0]: # Gana el jugador 2
            if usuario["idioma"] == "es-ES":
                cv2.putText(resultado, f"Ha ganado el jugador : 2", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            elif usuario["idioma"] == "en-US":
                cv2.putText(resultado, f"Player 2 has won", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            else:
                cv2.putText(resultado, f"Player 2 has won", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
        elif perdedor[1]: # Gana el jugador 1
            if usuario["idioma"] == "es-ES":
                cv2.putText(resultado, f"Ha ganado el jugador : 1", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            elif usuario["idioma"] == "en-US":
                cv2.putText(resultado, f"Player 1 has won", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            else:
                cv2.putText(resultado, f"Player 1 has won", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
        else:
            if usuario["idioma"] == "es-ES":
                cv2.putText(resultado, f"Jugador 1 tropa al frente: {tropa_delantera1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
                cv2.putText(resultado, f"Jugador 2 tropa al frente: {tropa_delantera2}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
                cv2.putText(resultado, f"Turno: {id_jugador}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            elif usuario["idioma"] == "en-US":
                cv2.putText(resultado, f"Player 1 front troop: {tropa_delantera1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
                cv2.putText(resultado, f"Player 2 front troop: {tropa_delantera2}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
                cv2.putText(resultado, f"Turn: {id_jugador}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
            else:
                cv2.putText(resultado, f"Player 1 front troop: {tropa_delantera1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
                cv2.putText(resultado, f"Player 2 front troop: {tropa_delantera2}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)
                cv2.putText(resultado, f"Turn: {id_jugador}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,128,128), 2)

    return resultado

ar.process = realidadMixta

try:
    ar.play("CUIA Álvaro García", key=ord(' '))
    while not exit_flag:
        continue 
finally:
    stop_listening(wait_for_stop=False)
    ar.release()
