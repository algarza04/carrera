<?php

require_once(__DIR__ . '/../config/funciones.php');
iniciar_sesion();
$pdo = obtener_pdo();

// Verificar que el usuario esté autenticado y sea administrador
if (!es_admin()) {
    redirigir_error('login', 'error', 'acceso');
}

// Verificar que se ha subido un archivo correctamente
if (!isset($_FILES['sql_file']) || $_FILES['sql_file']['error'] !== UPLOAD_ERR_OK) {
    redirigir_error('base_datos', 'error', 'upload');
}

// Leer contenido del archivo .sql
$contenido_sql = file_get_contents($_FILES['sql_file']['tmp_name']);
if (!$contenido_sql) {
    redirigir_error('base_datos', 'error', 'lectura');
}

// Separar las sentencias por punto y coma
$sentencias = array_filter(array_map('trim', explode(';', $contenido_sql)));

// Ejecutar cada sentencia individualmente
try {
    $pdo->beginTransaction();

    // Ejecutar múltiples sentencias SQL
    $pdo->exec($contenido_sql);

    $pdo->commit();
    registrar_evento("Se importó correctamente la base de datos.");
    redirigir_mensaje('base_datos', 'mensaje', 'restaurado_ok');

} catch (PDOException $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    registrar_evento("Error al importar la base de datos: " . $e->getMessage());
    redirigir_error('base_datos', 'error', 'sql');
}