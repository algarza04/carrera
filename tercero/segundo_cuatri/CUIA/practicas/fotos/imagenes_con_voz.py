import cv2
import numpy as np
import cuia
import speech_recognition as sr
import threading
import estado_de_juego

# Variables globales
id_jugador = 1
exit_flag = False
marcadores_seleccionados = 0
salir = False
imagen = cv2.cvtColor(cv2.imread("imagenes/negro.png"), cv2.COLOR_BGR2BGRA)
#almacenaremos vida, daño, habilidad de cada tropa y tipo de tropa
tropas = np.empty((4, 4))
imagenes = [imagen, imagen, imagen, imagen]
tropa_delantera1 = 0
tropa_delantera2 = 2

# --- VOZ ---
def voz_callback(recognizer, audio):
    global exit_flag, id_jugador, marcadores_seleccionados, imagenes, salir, ataque, tropa_delantera1, tropa_delantera2

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("Dijiste:", texto)

        # ETAPA 1: Selección de tropas (marcadores)
        if not salir:
            if "añadir dragón de fuego" in texto.lower():
                imagenes[marcadores_seleccionados] = (cv2.cvtColor(cv2.imread("imagenes/dragon_fuego.jpg"), cv2.COLOR_BGR2BGRA))
                estado_de_juego.crear_tropa(marcadores_seleccionados, 0, tropas)
                marcadores_seleccionados += 1
                print("Se añadió un Dragón de Fuego.")
            elif "añadir dragón de agua" in texto.lower():
                imagenes[marcadores_seleccionados] = (cv2.cvtColor(cv2.imread("imagenes/dragon_agua.jpg"), cv2.COLOR_BGR2BGRA))
                estado_de_juego.crear_tropa(marcadores_seleccionados, 1, tropas)
                marcadores_seleccionados += 1
                print("Se añadió un Dragón de Agua.")
            elif "añadir golem" in texto.lower():
                imagenes[marcadores_seleccionados] = (cv2.cvtColor(cv2.imread("imagenes/golem.png"), cv2.COLOR_BGR2BGRA))
                estado_de_juego.crear_tropa(marcadores_seleccionados, 2, tropas)
                marcadores_seleccionados += 1
                print("Se añadió un Gólem.")
            elif "añadir erizo" in texto.lower():
                imagenes[marcadores_seleccionados] = (cv2.cvtColor(cv2.imread("imagenes/erizo.png"), cv2.COLOR_BGR2BGRA))
                estado_de_juego.crear_tropa(marcadores_seleccionados, 3, tropas)
                marcadores_seleccionados += 1
                print("Se añadió un erizo.")
            else:
                print("Solo puedes añadir tropas ahora.")

            print(f"Marcadores seleccionados: {marcadores_seleccionados}/4")

            if marcadores_seleccionados >= 4:
                salir = True
                print("¡Todos los marcadores han sido seleccionados! Ahora puedes atacar.")

            return 

        # ETAPA 2: Solo se accede aquí después de seleccionar los 4 marcadores
        if "cambiar tropa delantera" in texto.lower():
            if id_jugador == 1:
                #si la tropa no cambia no va a pasar el turno al siguiente jugador
                tropa_principio = tropa_delantera1
                tropa_delantera1 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera1, id_jugador, tropas)
                if tropa_principio != tropa_delantera1:
                    id_jugador = 2
                else: 
                    print("No se puede cambiar a una tropa sin vida")
            else:
                #si la tropa no cambia no va a pasar el turno al siguiente jugador
                tropa_principio = tropa_delantera2
                tropa_delantera2 = estado_de_juego.cambiar_tropa_delantera(tropa_delantera2, id_jugador, tropas)
                if tropa_principio != tropa_delantera2:
                    id_jugador = 1
                else:
                    print("No se puede cambiar a una tropa sin vida")

        elif "atacar con la primera tropa" in texto.lower():
            if id_jugador == 1:
                estado_de_juego.atacar(0, tropa_delantera1, tropa_delantera2, id_jugador, tropas)
                id_jugador = 2
            else:
                estado_de_juego.atacar(2, tropa_delantera2, tropa_delantera1, id_jugador, tropas)
                id_jugador = 1

        elif "atacar con la segunda tropa" in texto.lower():
            if id_jugador == 1:
                estado_de_juego.atacar(1, tropa_delantera1, tropa_delantera2, id_jugador, tropas)
                id_jugador = 2
            else:
                estado_de_juego.atacar(3, tropa_delantera2, tropa_delantera1, id_jugador, tropas)
                id_jugador = 1

        elif "me rindo" in texto.lower():
            print("¡Jugador se rinde!")
            exit_flag = True

        #if 

    except sr.UnknownValueError:
        print("No se entendió el audio.")
    except sr.RequestError as e:
        print(f"Error con el servicio de voz: {e}")

# Iniciar escucha en segundo plano
r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)
    print("Micrófono calibrado. Escuchando...")
stop_listening = r.listen_in_background(m, voz_callback)

# --- CÁMARA y ARUCO ---
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
detector = cv2.aruco.ArucoDetector(diccionario)

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

ar = cuia.myVideo(cam, bk)

def origen(TAM):
    return(np.array([[-TAM/2.0, -TAM/2.0, 0.0],
                     [-TAM/2.0,  TAM/2.0, 0.0],
                     [ TAM/2.0,  TAM/2.0, 0.0],
                     [ TAM/2.0, -TAM/2.0, 0.0]]))

def proyeccion(puntos, rvec, tvec, cameraMatrix, distCoeffs):
    if isinstance(puntos, list):
        return(proyeccion(np.array(puntos, dtype=np.float32), rvec, tvec, cameraMatrix, distCoeffs))
    if isinstance(puntos, np.ndarray):
        if puntos.ndim == 1 and puntos.size == 3:
            res, _ = cv2.projectPoints(puntos.astype(np.float32), rvec, tvec, cameraMatrix, distCoeffs)
            return(res[0][0].astype(int))
        if puntos.ndim > 1:
            aux = proyeccion(puntos[0], rvec, tvec, cameraMatrix, distCoeffs)
            aux = np.expand_dims(aux, axis=0)
            for p in puntos[1:]:
                aux = np.append(aux, [proyeccion(p, rvec, tvec, cameraMatrix, distCoeffs)], axis=0)
            return(np.array(aux))

def variasimagenes(frame):
    framebgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    hframe, wframe, _ = frame.shape
    tam = 0.1
    bboxs, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        res = framebgra
        for i in range(len(ids)):
            ret, rvec, tvec = cv2.solvePnP(origen(tam), bboxs[i], cameraMatrix, distCoeffs)
            if ret:
                imagen = imagenes[ids[i][0]]

                # Verifica si la vida de la tropa es menor o igual a 0
                if tropas[ids[i][0]][0] <= 0:
                    gris = cv2.cvtColor(imagen[:, :, :3], cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
                    gris_color = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGRA)  # Volver a BGRA (con canal alfa)
                    gris_color[:, :, 3] = imagen[:, :, 3]  # Mantener canal alfa original
                    imagen = gris_color

                h, w, _ = imagen.shape
                desde = np.array([[0,0],[w,0],[w,h],[0,h]])
                hasta = proyeccion(origen(tam), rvec, tvec, cameraMatrix, distCoeffs)
                M = cv2.getPerspectiveTransform(np.float32(desde), np.float32(hasta))
                warp = cv2.warpPerspective(imagen, M, dsize=(wframe,hframe))
                res = cuia.alphaBlending(warp, res)
    else:
        res = frame

    # Mostrar vida como texto en la esquina superior izquierda
    cv2.putText(res, f"Vida1: {tropas[0][0]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(res, f"Vida2: {tropas[1][0]}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(res, f"Vida3: {tropas[2][0]}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(res, f"Vida4: {tropas[3][0]}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(res, f"Tropa delante: {tropa_delantera1}", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(res, f"Tropa delante 2 : {tropa_delantera2}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)



    return res

ar.process = variasimagenes

try:
    ar.play("Varias imágenes + Voz", key=ord(' '))
    while not exit_flag:
        continue  # Loop de espera para que la voz se escuche mientras la ventana esté abierta
finally:
    stop_listening(wait_for_stop=False)
    ar.release()
