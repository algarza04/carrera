<?php

/**
 * Página para buscar reservas
 * Permite filtrar y ordenar reservas por diferentes criterios.
 */
require_once 'config/funciones.php';
iniciar_sesion();

$pdo = obtener_pdo();

$campos = ['motivo', 'fecha_inicio', 'fecha_fin', 'usuarios', 'salas', 'ordenar_por', 'items_por_pagina'];
foreach ($campos as $campo) {
    if (isset($_GET[$campo])) {
        setcookie($campo, is_array($_GET[$campo]) ? json_encode($_GET[$campo]) : $_GET[$campo], time() + 3600);
    } elseif (isset($_COOKIE[$campo])) {
        $_GET[$campo] = in_array($campo, ['usuarios', 'salas']) ? json_decode($_COOKIE[$campo], true) : $_COOKIE[$campo];
    }
}

$motivo = $_GET['motivo'] ?? '';
$fecha_inicio = $_GET['fecha_inicio'] ?? '';
$fecha_fin = $_GET['fecha_fin'] ?? '';
$usuarios = $_GET['usuarios'] ?? [];
$salas = array_filter($_GET['salas'] ?? [], fn($s) => is_numeric($s) && $s > 0);
$ordenar_por = $_GET['ordenar_por'] ?? 'fecha';
$items_por_pagina = max(1, (int)($_GET['items_por_pagina'] ?? 5));
$pagina_actual = max(1, (int)($_GET['pagina'] ?? 1));
$es_admin = isset($_SESSION['rol']) && $_SESSION['rol'] === 'admin';
$usuario_id = $_SESSION['id'] ?? null;

// Construcción de la consulta
$sql = "SELECT r.*, u.nombre AS usuario_nombre, s.nombre AS sala_nombre
        FROM reservas r
        JOIN usuarios u ON r.usuario_id = u.id
        JOIN salas s ON r.sala_id = s.id
        WHERE 1=1";
$params = [];

if (!$es_admin && $usuario_id) {
    $sql .= " AND r.usuario_id = ?";
    $params[] = $usuario_id;
}

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
if (!empty($usuarios) && $es_admin) {
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

// Paginación
$total_sql = "SELECT COUNT(*) FROM ($sql) AS subconsulta";
$stmt = $pdo->prepare($total_sql);
$stmt->execute($params);
$total_resultados = $stmt->fetchColumn();

$offset = ($pagina_actual - 1) * $items_por_pagina;
$sql .= " LIMIT $items_por_pagina OFFSET $offset";

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$reservas = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Datos para los select
$usuarios_lista = $pdo->query("SELECT id, nombre FROM usuarios")->fetchAll(PDO::FETCH_ASSOC);
$salas_lista = $pdo->query("SELECT id, nombre FROM salas")->fetchAll(PDO::FETCH_ASSOC);
?>

<form method="get" action="index.php" novalidate>
    <input type="hidden" name="page" value="listar_reservas">
    
    <label>Motivo:
        <input type="text" name="motivo" value="<?= htmlspecialchars($motivo) ?>" style="width:150px;">
    </label>

    <label>Fecha inicial:
        <input type="date" name="fecha_inicio" value="<?= htmlspecialchars($fecha_inicio) ?>">
    </label>

    <label>Fecha final:
        <input type="date" name="fecha_fin" value="<?= htmlspecialchars($fecha_fin) ?>">
    </label>

    <?php if ($es_admin): ?>
        <label>Usuario:
            <select name="usuarios[]" multiple size="3" style="width:150px;">
                <?php foreach ($usuarios_lista as $u): ?>
                    <option value="<?= $u['id'] ?>" <?= in_array($u['id'], $usuarios) ? 'selected' : '' ?>>
                        <?= htmlspecialchars($u['nombre']) ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </label>
    <?php else: ?>
        <label>Usuario:
            <select readonly style="width:150px; background:#eee;">
                <?php
                    $usuario_nombre = '';
                    foreach ($usuarios_lista as $u) {
                        if ($u['id'] == $usuario_id) {
                            $usuario_nombre = $u['nombre'];
                            break;
                        }
                    }
                ?>
                <option value="<?= $usuario_id ?>" selected><?= htmlspecialchars($usuario_nombre) ?></option>
            </select>
            <input type="hidden" name="usuarios[]" value="<?= $usuario_id ?>">
        </label>
    <?php endif; ?>

    <label>Sala:
        <select name="salas[]" multiple size="3" style="width:150px;">
            <?php foreach ($salas_lista as $s): ?>
                <option value="<?= $s['id'] ?>" <?= in_array($s['id'], $salas) ? 'selected' : '' ?>>
                    <?= htmlspecialchars($s['nombre']) ?>
                </option>
            <?php endforeach; ?>
        </select>
    </label>
    
    <label>Ordenar por:
        <p style="margin:0; padding:0;">
        <label><input type="radio" name="ordenar_por" value="fecha" <?= $ordenar_por === 'fecha' ? 'checked' : '' ?>> Fecha y hora</label>
        <label><input type="radio" name="ordenar_por" value="sala" <?= $ordenar_por === 'sala' ? 'checked' : '' ?>> Sala</label>
        </p>
    </label>
    
    <label>Ítems por página:
        <input type="number" name="items_por_pagina" value="<?= htmlspecialchars($items_por_pagina) ?>" min="1" style="width:50px;">
    </label>
    
    <button type="submit" class="boton">
        Aplicar criterios de búsqueda y ordenación
    </button>
</form>
