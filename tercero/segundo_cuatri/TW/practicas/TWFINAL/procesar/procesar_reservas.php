<?php
/**
 * Fichero para procesar las resrevas de salas
 */
require_once '../config/funciones.php';
iniciar_sesion();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $pdo = obtener_pdo();
    $sala_id = $_POST['sala_id'];
    $fecha = $_POST['fecha'];
    $hora_inicio = $_POST['hora_inicio'];
    $hora_fin = $_POST['hora_fin'];
    $motivo = $_POST['motivo'];

    // Verificar solapamiento
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM reservas WHERE sala_id = ? AND fecha = ? AND (
        (hora_inicio < ? AND hora_fin > ?) OR
        (hora_inicio >= ? AND hora_inicio < ?)
    )");
    $stmt->execute([$sala_id, $fecha, $hora_fin, $hora_inicio, $hora_inicio, $hora_fin]);
    $solapadas = $stmt->fetchColumn();

    if ($solapadas > 0) {
        header("Location: ../index.php?page=reservas&fecha=$fecha&error=solapada");
        exit;
    }

    // Insertar reserva
    $stmt = $pdo->prepare("INSERT INTO reservas (sala_id, usuario_id, fecha, hora_inicio, hora_fin, motivo) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->execute([$sala_id, $_SESSION['id'], $fecha, $hora_inicio, $hora_fin, $motivo]);

    header("Location: ../index.php?page=reservas&fecha=$fecha&ok=1");
    exit;
}
?>