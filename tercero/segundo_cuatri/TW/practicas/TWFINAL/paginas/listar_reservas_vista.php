<?php
/**
 * Pagina para listar las reservas de salas
 * Permite filtrar por fecha, sala y usuario.
 * Muestra los resultados paginados.
 */
// Carga los datos procesados
extract(require __DIR__ . '/../procesar/listar_reservas.php');
?>

<h2>Resultados de la búsqueda</h2>
<p>Total de reservas encontradas: <?= $total_resultados ?></p>

<table style="border-collapse:collapse; width:70%; margin-top:15px; font-size:1.1em;">
    <tr style="background:#ffe0b2;">
        <th>Fecha</th>
        <th>Horas</th>
        <th>Sala</th>
        <th>Usuario</th>
        <th>Motivo</th>
    </tr>
    <?php foreach ($reservas as $r): ?>
        <tr>
            <td><?= date('d/m/Y', strtotime($r['fecha'])) ?></td>
            <td><?= htmlspecialchars($r['hora_inicio']) ?> - <?= htmlspecialchars($r['hora_fin']) ?></td>
            <td><?= htmlspecialchars($r['sala_nombre']) ?></td>
            <td><?= htmlspecialchars($r['usuario_nombre']) ?></td>
            <td><?= htmlspecialchars($r['motivo']) ?></td>
        </tr>
    <?php endforeach; ?>
</table>

<?php if ($total_paginas > 1): ?>
    <div style="margin:15px 0;">
        <?php if ($pagina_actual > 1): ?>
            <a href="?<?= http_build_query(array_merge($_GET, ['pagina' => 1])) ?>" style="font-size:1.2em;">&#9664;&#9664;</a>
            <a href="?<?= http_build_query(array_merge($_GET, ['pagina' => $pagina_actual-1])) ?>" style="font-size:1.2em;">&#9664;</a>
        <?php endif; ?>
        <strong>Página <?= $pagina_actual ?> de <?= $total_paginas ?></strong>
        <?php if ($pagina_actual < $total_paginas): ?>
            <a href="?<?= http_build_query(array_merge($_GET, ['pagina' => $pagina_actual+1])) ?>" style="font-size:1.2em;">&#9654;</a>
            <a href="?<?= http_build_query(array_merge($_GET, ['pagina' => $total_paginas])) ?>" style="font-size:1.2em;">&#9654;&#9654;</a>
        <?php endif; ?>
    </div>
<?php endif; ?>