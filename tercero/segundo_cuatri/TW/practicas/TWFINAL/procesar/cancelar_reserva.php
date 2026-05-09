<?php

/**
 * Fichero para procesar la cancelación de una reserva
 * Elimina la reserva seleccionada y redirige a la página de reservas.
 */
require_once '../config/funciones.php';
iniciar_sesion();

$pdo = obtener_pdo();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['reserva_id'])) {
    $reserva_id = $_POST['reserva_id'];
    // Opcional: puedes comprobar que la reserva pertenece al usuario logueado o es admin
    $stmt = $pdo->prepare("DELETE FROM reservas WHERE id = ?");
    $stmt->execute([$reserva_id]);
}

$fecha = $_POST['fecha'] ?? date('Y-m-d');
header("Location: ../index.php?page=reservas&fecha=" . urlencode($fecha) . "&aceptar_fecha=1");
exit;
?>