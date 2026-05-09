import face_recognition
import cv2
import json
import os
import numpy as np
import speech_recognition as sr

RUTA_JSON = "usuarios.json"

def cargar_usuarios():
    if not os.path.exists(RUTA_JSON):
        return {"ids": [], "nombres": [], "encodings": [], "favoritos": {}, "idiomas": {}}
    with open(RUTA_JSON, "r") as f:
        data = json.load(f)
    if "ids" not in data:
        data["ids"] = list(range(1, len(data.get("nombres", [])) + 1))
    if "nombres" not in data:
        data["nombres"] = []
    if "encodings" not in data:
        data["encodings"] = []
    if "favoritos" not in data:
        data["favoritos"] = {}
    if "idiomas" not in data: 
        data["idiomas"] = {}
    data["encodings"] = [np.array(enc) for enc in data["encodings"]]
    return data

def guardar_usuario(nombre, encoding):
    usuarios = cargar_usuarios()

    usuarios["encodings"] = [
        enc.tolist() if isinstance(enc, np.ndarray) else enc
        for enc in usuarios["encodings"]
    ]

    if isinstance(encoding, np.ndarray):
        encoding = encoding.tolist()

    nuevo_id = max(usuarios["ids"], default=0) + 1

    usuarios["ids"].append(nuevo_id)
    usuarios["nombres"].append(nombre)
    usuarios["encodings"].append(encoding)
    usuarios["favoritos"][str(nuevo_id)] = []  # Lista vacía por defecto
    usuarios["idiomas"][str(nuevo_id)] = "es-ES"

    try:
        with open("usuarios_tmp.json", "w") as f:
            json.dump(usuarios, f, indent=4)
        os.replace("usuarios_tmp.json", RUTA_JSON)
        print(f"Usuario {nombre} (ID: {nuevo_id}) registrado correctamente.")
    except Exception as e:
        print(f"Error al guardar usuario: {e}")

def guardar_favorito(id_usuario, favoritas):
    usuarios = cargar_usuarios()
    
    if id_usuario not in usuarios["ids"]:
        print(f"Usuario con ID {id_usuario} no encontrado.")
        return

    if not isinstance(favoritas, list):
        print("Favoritas debe ser una lista de tropas.")
        return

    usuarios["favoritos"][str(id_usuario)] = favoritas[:4]

    try:
        with open("usuarios_tmp.json", "w") as f:
            json.dump({
                "ids": usuarios["ids"],
                "nombres": usuarios["nombres"],
                "encodings": [enc.tolist() for enc in usuarios["encodings"]],
                "favoritos": usuarios["favoritos"],
                "idiomas": usuarios["idiomas"],
            }, f, indent=4)
        os.replace("usuarios_tmp.json", RUTA_JSON)
        print(f"Favoritas guardadas para ID {id_usuario}: {usuarios['favoritos'][str(id_usuario)]}")
    except Exception as e:
        print(f"Error al guardar favoritas: {e}")

def guardar_idioma(id_usuario, idioma):
    usuarios = cargar_usuarios()
    
    if id_usuario not in usuarios["ids"]:
        print(f"Usuario con ID {id_usuario} no encontrado.")
        return

    usuarios["idiomas"][str(id_usuario)] = idioma

    try:
        with open("usuarios_tmp.json", "w") as f:
            json.dump({
                "ids": usuarios["ids"],
                "nombres": usuarios["nombres"],
                "encodings": [
                    enc.tolist() if isinstance(enc, np.ndarray) else enc
                    for enc in usuarios["encodings"]
                ],
                "favoritos": usuarios["favoritos"],
                "idiomas": usuarios["idiomas"],
            }, f, indent=4)
        os.replace("usuarios_tmp.json", RUTA_JSON)
        print(f"Idioma '{idioma}' guardado para el usuario ID {id_usuario}.")
    except Exception as e:
        print(f"Error al guardar el idioma: {e}")

def cargar_favorito(id_usuario):
    usuarios = cargar_usuarios()
    return usuarios.get("favoritos", {}).get(str(id_usuario), [])

def capturar_nombre_por_voz():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Por favor, di tu nombre...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            nombre = recognizer.recognize_google(audio, language="es-ES")
            print(f"Nombre reconocido: {nombre}")
            return nombre
        except sr.UnknownValueError:
            print("No entendí tu nombre. Intenta de nuevo.")
            return capturar_nombre_por_voz()
        except sr.WaitTimeoutError:
            print("No se detectó voz. Intenta de nuevo.")
            return capturar_nombre_por_voz()
        except sr.RequestError as e:
            print(f"Error con el servicio de voz: {e}")
            return None

def reconocer_o_registrar():
    cap = cv2.VideoCapture(0)
    usuarios = cargar_usuarios()
    print("Esperando detección de rostro...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locs)

        for encoding in encodings:
            if usuarios["encodings"]:
                matches = face_recognition.compare_faces(usuarios["encodings"], encoding)
                if True in matches:
                    i = matches.index(True)
                    nombre = usuarios["nombres"][i]
                    id_usuario = usuarios["ids"][i]
                    favoritas = usuarios["favoritos"].get(str(id_usuario), [])
                    idioma = usuarios["idiomas"].get(str(id_usuario), "es-ES")
                    print(f"Usuario reconocido: {nombre} (ID: {id_usuario})")
                    cap.release()
                    cv2.destroyAllWindows()
                    # AQUI ES DONDE SE CORRIGE EL ERROR: Añadir 'idioma' al diccionario de retorno
                    return {"id": id_usuario, "nombre": nombre, "favoritas": favoritas, "idioma": idioma}

            cv2.imshow("Nuevo usuario detectado", frame)
            print("Usuario no reconocido.")
            nombre = capturar_nombre_por_voz()
            if nombre:
                guardar_usuario(nombre, encoding)
                cap.release()
                cv2.destroyAllWindows()
                usuarios = cargar_usuarios()
                i = len(usuarios["nombres"]) - 1
                return {
                    "id": usuarios["ids"][i],
                    "nombre": nombre,
                    "favoritas": usuarios["favoritos"].get(str(usuarios["ids"][i]), []),
                    "idioma": usuarios["idiomas"].get(str(usuarios["ids"][i]), "es-ES")
                }

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None