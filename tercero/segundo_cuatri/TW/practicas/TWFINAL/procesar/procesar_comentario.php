<?php
require_once '../config/funciones.php';
iniciar_sesion();

$pdo = obtener_pdo();
$usuario_id = $_SESSION['id'] ?? null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_SESSION['id'])) {
    $sala_id = $_POST['sala_id'] ?? null;
    $texto = trim($_POST['texto'] ?? '');

    if ($sala_id && $texto !== '') {
        $stmt = $pdo->prepare("INSERT INTO comentarios (sala_id, usuario_id, texto) VALUES (?, ?, ?)");
        $stmt->execute([$sala_id, $usuario_id, $texto]);
    }
}

header("Location: ../index.php?page=sala&id=" . urlencode($sala_id));
exit;

?>