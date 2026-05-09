<?php
/**
 * Pagina para listar las salas del centro docente
 * Muestra un listado de todas las salas con enlaces para ver detalles, editar o borrar.
 * Solo los administradores pueden editar o borrar salas.
 * Se puede borrar una sala aunque tenga resrvas
 */
require_once 'config/funciones.php';

iniciar_sesion();
$pdo = obtener_pdo();

// Consulta para obtener todas las salas
$stmt = $pdo->query("SELECT * FROM salas");
$salas = $stmt->fetchAll();

?>

<h2>Listado de Salas</h2>
<ul>
    <?php foreach ($salas as $sala): ?>
        <li>
            <a href="index.php?page=sala&id=<?= $sala['id'] ?>">
                <?= htmlspecialchars($sala['nombre']) ?> (<?= htmlspecialchars($sala['ubicacion']) ?>)
            </a>
            <?php if (es_admin()): ?>
                <a href="index.php?page=editar_sala&id=<?= $sala['id'] ?>">Editar</a>
                <?php
                // Comprobar si la sala tiene reservas
                $stmt = $pdo->prepare("SELECT COUNT(*) FROM reservas WHERE sala_id = ?");
                $stmt->execute([$sala['id']]);
                $reservas_count = $stmt->fetchColumn();
                ?>
                <?php if ($reservas_count > 0): ?>
                    <a href="procesar/borrar_sala.php?id=<?= $sala['id'] ?>"
                        onclick="return confirm('Esta sala tiene reservas asociadas. ¿Seguro que quieres borrarla?')">Borrar</a>
                <?php else: ?>
                    <a href="procesar/borrar_sala.php?id=<?= $sala['id'] ?>"
                        onclick="return confirm('¿Seguro que quieres borrar esta sala?')">Borrar</a>
                <?php endif; ?>
            <?php endif; ?>
        </li>
    <?php endforeach; ?>
</ul>
