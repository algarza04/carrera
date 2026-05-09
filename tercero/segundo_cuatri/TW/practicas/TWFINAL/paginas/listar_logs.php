<?php
/**
 * Pagina para listar los eventos del log del sistema
 * Solo accesible por administradores.
 * Muestra los eventos registrados en el sistema ordenados por fecha y hora.
 */
require_once 'config/funciones.php';
iniciar_sesion();

if (!es_admin()) {
    header("Location: index.php?page=inicio&error=permiso_denegado");
    exit;
}

$pdo = obtener_pdo();
$stmt = $pdo->query("SELECT * FROM log ORDER BY fecha_hora DESC");
$logs = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<h2>Listado de Eventos</h2>
<table>
    <thead>
        <tr>
            <th style="color: black;">Fecha y Hora</th>
            <th style="color: black;">Descripción</th>
        </tr>
    </thead>
    <tbody>
        <?php foreach ($logs as $log): ?>
            <tr>
                <td><?= htmlspecialchars($log['fecha_hora']) ?></td>
                <td><?= htmlspecialchars($log['descripcion']) ?></td>
            </tr>
        <?php endforeach; ?>
    </tbody>
</table>
<a href="index.php?page=inicio">Volver</a>