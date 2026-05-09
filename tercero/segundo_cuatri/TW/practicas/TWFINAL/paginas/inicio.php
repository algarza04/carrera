<?php
/** 
 * Página de inicio del sistema
 * Muestra información general y eventos de interés del centro docente.
*/
require_once 'config/funciones.php';

$pdo = obtener_pdo();

// Obtener la configuración del centro
$stmt = $pdo->query("SELECT descripcion, hora_apertura, hora_cierre FROM configuracion_centro LIMIT 1");
$configuracion = $stmt->fetch(PDO::FETCH_ASSOC);
?>

<section>
    <h2>Bienvenido al Centro Docente</h2>
    <p><?= htmlspecialchars($configuracion['descripcion']) ?></p>
</section>

<section>
    <p><strong>Horario de apertura:</strong> <?= htmlspecialchars($configuracion['hora_apertura']) ?> - <?= htmlspecialchars($configuracion['hora_cierre']) ?></p>
</section>