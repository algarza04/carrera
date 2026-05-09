import cv2

# Alias al submódulo aruco
aruco = cv2.aruco

# Diccionario 5×5 con 50 marcadores
dic = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)

# ID y tamaño en píxeles
marker_id   = 4
side_pixels = 170

# Genera la imagen del marcador (diccionario, id, tamaño)
marker_img = aruco.generateImageMarker(dic, marker_id, side_pixels)

# Guárdalo como PNG
cv2.imwrite("marker0.png", marker_img)
print(f"✔ marker{marker_id}.png generado ({side_pixels}×{side_pixels}px)")
