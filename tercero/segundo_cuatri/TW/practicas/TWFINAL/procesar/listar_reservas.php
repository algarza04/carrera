<?php
/**
 * Ficjero para listar reservas
 * Permite filtrar por motivo, fecha, usuario y sala.
 * Muestra los resultados paginados.
 */
require_once 'config/funciones.php';
iniciar_sesion();

$motivo = $_GET['motivo'] ?? '';
$fecha_inicio = $_GET['fecha_inicio'] ?? '';
$fecha_fin = $_GET['fecha_fin'] ?? '';
$usuarios = $_GET['usuarios'] ?? [];
$salas = $_GET['salas'] ?? [];
$ordenar_por = $_GET['ordenar_por'] ?? 'fecha';
$items_por_pagina = max(1, (int)($_GET['items_por_pagina'] ?? 5));
$pagina_actual = max(1, (int)($_GET['pagina'] ?? 1));

$pdo = obtener_pdo();

$sql = "SELECT r.*, u.nombre AS usuario_nombre, s.nombre AS sala_nombre
        FROM reservas r
        JOIN usuarios u ON r.usuario_id = u.id
        JOIN salas s ON r.sala_id = s.id
        WHERE 1=1";
$params = [];

if ($motivo !== '') {
    $sql .= " AND r.motivo LIKE ?";
    $params[] = "%$motivo%";
}
if ($fecha_inicio) {
    $sql .= " AND r.fecha >= ?";
    $params[] = $fecha_inicio;
}
if ($fecha_fin) {
    $sql .= " AND r.fecha <= ?";
    $params[] = $fecha_fin;
}
if (!empty($usuarios)) {
    $placeholders = implode(',', array_fill(0, count($usuarios), '?'));
    $sql .= " AND r.usuario_id IN ($placeholders)";
    $params = array_merge($params, $usuarios);
}
if (!empty($salas)) {
    $placeholders = implode(',', array_fill(0, count($salas), '?'));
    $sql .= " AND r.sala_id IN ($placeholders)";
    $params = array_merge($params, $salas);
}

$sql .= $ordenar_por === 'sala' ? " ORDER BY s.nombre" : " ORDER BY r.fecha";

$total_sql = "SELECT COUNT(*) FROM ($sql) AS subconsulta";
$stmt = $pdo->prepare($total_sql);
$stmt->execute($params);
$total_resultados = $stmt->fetchColumn();

$offset = ($pagina_actual - 1) * $items_por_pagina;
$sql .= " LIMIT $items_por_pagina OFFSET $offset";

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$reservas = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Paginación
$total_paginas = ceil($total_resultados / $items_por_pagina);

// Devuelve los datos para la vista
return [
    'reservas' => $reservas,
    'total_resultados' => $total_resultados,
    'pagina_actual' => $pagina_actual,
    'total_paginas' => $total_paginas,
];