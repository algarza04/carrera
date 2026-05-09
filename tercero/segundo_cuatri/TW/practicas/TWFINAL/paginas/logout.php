<?php
/**
 * Pagina para cerrar sesión
 * Registra el evento de cierre de sesión y destruye la sesión.
 */
include_once '../config/funciones.php';

session_start();
registrar_evento("El usuario " . $_SESSION['email'] . " cerró sesión: ");
session_unset();
session_destroy();
header("Location: index.php?page=login");
exit;
?>
