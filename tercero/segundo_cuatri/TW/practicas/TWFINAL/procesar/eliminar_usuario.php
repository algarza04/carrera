<?php
/**
 * Fichero para eliminar un usuario
 * Verifica permisos de administrador y elimina el usuario seleccionado.
 * Redirige a la lista de usuarios con mensajes de éxito o error.
 */
require_once '../config/funciones.php';
iniciar_sesion();

// Verificar si el usuario es administrador
if (!es_admin()) {
    header("Location: ../index.php?page=inicio&error=permiso");
    exit;
}

// Verificar si se ha enviado el ID del usuario
if (!isset($_GET['id']) || empty($_GET['id'])) {
    header("Location: ../index.php?page=listar_usuarios&error=id_invalido");
    exit;
}

$id = $_GET['id'];

try {
    $pdo = obtener_pdo();

    // Comprobar si el usuario existe
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM usuarios WHERE id = ?");
    $stmt->execute([$id]);
    if ($stmt->fetchColumn() == 0) {
        header("Location: ../index.php?page=listar_usuarios&error=usuario_no_existe");
        exit;
    }

    // Eliminar el usuario
    $stmt = $pdo->prepare("DELETE FROM usuarios WHERE id = ?");
    $stmt->execute([$id]);

    // Redirigir con éxito
    header("Location: ../index.php?page=listar_usuarios&ok=usuario_eliminado");
    exit;
} catch (PDOException $e) {
    // Manejar errores de la base de datos
    header("Location: ../index.php?page=listar_usuarios&error=db_error");
    exit;
}