<?php
/**
 * Fichero para guardar la configuración del centro
 * Permite actualizar el nombre, descripción, horarios y logotipo del centro.
 * Requiere permisos de administrador.
 * Redirige a la página de inicio con mensajes de éxito o error.
 */
require_once('../config/funciones.php');
iniciar_sesion();
if (!es_admin()) {
    header("Location: ../index.php?page=inicio&error=acceso_restringido");
    exit;
}

$nombre = trim($_POST['nombre'] ?? '');
$descripcion = trim($_POST['descripcion'] ?? '');
$hora_apertura = $_POST['hora_apertura'] ?? null;
$hora_cierre = $_POST['hora_cierre'] ?? null;

// Actualiza la configuración general
$sql = "UPDATE configuracion_centro SET nombre = ?, descripcion = ?, hora_apertura = ?, hora_cierre = ? WHERE id = 1";
$stmt = $conexion->prepare($sql);
$stmt->bind_param("ssss", $nombre, $descripcion, $hora_apertura, $hora_cierre);
$stmt->execute();

// Procesar logotipo si se sube
if (isset($_FILES['logotipo']) && $_FILES['logotipo']['error'] === UPLOAD_ERR_OK) {
    $tmp_name = $_FILES['logotipo']['tmp_name'];
    $mime_type = mime_content_type($tmp_name);
    $contenido = file_get_contents($tmp_name);

    // Guarda la imagen en la carpeta
    $nombre_archivo = 'logo_' . time() . '_' . basename($_FILES['logotipo']['name']);
    $ruta_destino = "../imagenes/centro/" . $nombre_archivo;
    move_uploaded_file($tmp_name, $ruta_destino);

    // Guarda o actualiza en la tabla fotos (referencia_id=1, tipo='logotipo')
    $stmt = $conexion->prepare("SELECT id FROM fotos WHERE referencia_id = 1 AND tipo = 'logotipo'");
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        // Actualiza
        $stmt = $conexion->prepare("UPDATE fotos SET contenido = ?, mime_type = ? WHERE referencia_id = 1 AND tipo = 'logotipo'");
        $stmt->bind_param("bs", $contenido, $mime_type);
        $stmt->send_long_data(0, $contenido);
        $stmt->execute();
    } else {
        // Inserta
        $stmt = $conexion->prepare("INSERT INTO fotos (referencia_id, tipo, contenido, mime_type) VALUES (1, 'logotipo', ?, ?)");
        $stmt->bind_param("bs", $contenido, $mime_type);
        $stmt->send_long_data(0, $contenido);
        $stmt->execute();
    }
}

header("Location: ../index.php?page=inicio&exito=1");
exit;
?>