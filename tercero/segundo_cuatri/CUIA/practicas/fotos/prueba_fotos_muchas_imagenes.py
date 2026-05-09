import cv2
import numpy as np
import cuia
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

detector = cv2.aruco.ArucoDetector(diccionario)

cam = 2
#Seleccionamos el mejor backend
bk = cuia.bestBackend(cam);

webcam = cv2.VideoCapture(cam, bk)

ancho = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

webcam.release()

# Intentamos importar los parámetros de calibración
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

baboon = cv2.imread("madrid.jpg")
apple = cv2.imread("montaña.jpg")
chicky = cv2.imread("pinguino.jpg")

imagenes = [cv2.cvtColor(baboon, cv2.COLOR_BGR2BGRA), cv2.cvtColor(apple, cv2.COLOR_BGR2BGRA), cv2.cvtColor(chicky, cv2.COLOR_BGR2BGRA)]

def variasimagenes(frame):
    framebgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    hframe, wframe, _ = frame.shape
    tam = 0.1 #Tamaño (en metros) del lado del marcador
    bboxs, ids, _ = detector.detectMarkers(frame)
    if ids is not None:
        res = framebgra
        for i in range(len(ids)):
            ret, rvec, tvec = cv2.solvePnP(origen(tam), bboxs[i], cameraMatrix, distCoeffs) 
            if ret:    
                imagen = imagenes[ids[i][0]]
                h, w, _ = imagen.shape
                desde = np.array([[0,0],[w,0],[w,h],[0,h]])
                hasta = proyeccion(origen(tam), rvec, tvec, cameraMatrix, distCoeffs)
                M = cv2.getPerspectiveTransform(np.float32(desde), np.float32(hasta))
                warp = cv2.warpPerspective(imagen, M, dsize=(wframe,hframe))
                res = cuia.alphaBlending(warp, res)
    else:
        res = frame
    return(res)

ar.process = variasimagenes
try:
    ar.play("Varias imágenes", key=ord(' '))
finally:
    ar.release()