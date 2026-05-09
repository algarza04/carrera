<?php
/**
 * Fichero para procesar la eliminación de una sala
 * Verifica permisos de administrador y elimina la sala seleccionada.
 * Redirige a la lista de salas con mensajes de éxito o error.
 */
require_once '../config/funciones.php';
iniciar_sesion();

// Verificar si el usuario es administrador
if (!es_admin()) {
    header("Location: ../index.php?page=listar_salas&error=permiso");
    exit;
}

// Verificar si se ha enviado el ID de la sala
if (!isset($_GET['id']) || empty($_GET['id'])) {
    header("Location: ../index.php?page=listar_salas&error=id_invalido");
    exit;
}

$sala_id = $_GET['id'];

try {
    $pdo = obtener_pdo();

    // Comprobar si la sala existe
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM salas WHERE id = ?");
    $stmt->execute([$sala_id]);
    if ($stmt->fetchColumn() == 0) {
        header("Location: ../index.php?page=listar_salas&error=sala_no_existe");
        exit;
    }

    // Eliminar la sala
    $stmt = $pdo->prepare("DELETE FROM salas WHERE id = ?");
    $stmt->execute([$sala_id]);

    // Redirigir con éxito
    header("Location: ../index.php?page=listar_salas&ok=sala_borrada");
    exit;
} catch (PDOException $e) {
    // Manejar errores de la base de datos
    header("Location: ../index.php?page=listar_salas&error=db_error");
    exit;
}