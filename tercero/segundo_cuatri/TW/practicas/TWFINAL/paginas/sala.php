<?php
/**
 * Pagina para mostrar una sala específica
 * Muestra los detalles de la sala, fotografías y comentarios.
 * Permite a los usuarios registrados comentar sobre la sala.
 */
require_once 'config/funciones.php';
iniciar_sesion();
$pdo = obtener_pdo();

$id = $_GET['id'] ?? null;
if (!$id) {
    header("Location: index.php?page=listar_salas");
    exit;
}

$stmt = $pdo->prepare("SELECT * FROM salas WHERE id = ?");
$stmt->execute([$id]);
$sala = $stmt->fetch(PDO::FETCH_ASSOC);
if (!$sala) {
    echo "Sala no encontrada";
    exit;
}

$errores = [];
if (trim($sala['nombre']) === '') {
    $errores[] = "El nombre de la sala es obligatorio.";
}
if (trim($sala['ubicacion']) === '') {
    $errores[] = "La ubicación de la sala es obligatoria.";
}
if (intval($sala['puestos']) < 1) {
    $errores[] = "El número de asientos debe ser mayor que 0.";
}

if (!empty($errores)) {
    echo '<div style="color:red;"><ul>';
    foreach ($errores as $error) {
        echo '<li>' . htmlspecialchars($error) . '</li>';
    }
    echo '</ul></div>';
    exit;
}

$stmt = $pdo->prepare("SELECT * FROM fotos WHERE referencia_id = ? AND tipo = 'sala'");
$stmt->execute([$id]);
$fotos = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Comentarios
$stmt = $pdo->prepare("
    SELECT c.texto, c.fecha, u.email FROM comentarios c
    JOIN usuarios u ON c.usuario_id = u.id
    WHERE c.sala_id = ?
    ORDER BY c.fecha DESC
");
$stmt->execute([$id]);
$comentarios = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<h2><?= htmlspecialchars($sala['nombre']) ?></h2>
<p><strong>Ubicación:</strong> <?= htmlspecialchars($sala['ubicacion']) ?></p>
<p><strong>Puestos disponibles:</strong> <?= $sala['puestos'] ?></p>
<p><strong>Descripción:</strong> <?= nl2br(htmlspecialchars($sala['descripcion'])) ?></p>
<p><strong>Reservable:</strong> <?= $sala['reservable'] ? 'Sí' : 'No' ?></p>

<h2>Fotografías</h2>
<?php if (count($fotos) > 0): ?>
    <div class="fotos-sala">
        <?php foreach ($fotos as $foto): ?>
            <img src="<?= htmlspecialchars($foto['ruta_foto']) ?>" alt="Foto de sala" style="max-width:200px; margin:5px;">
        <?php endforeach; ?>
    </div>
<?php else: ?>
    <p>No hay fotografías.</p>
<?php endif; ?>

<h2>Comentarios</h2>
<?php if (count($comentarios) > 0): ?>
    <ul class="comentarios">
        <?php foreach ($comentarios as $comentario): ?>
            <li>
                <strong><?= htmlspecialchars($comentario['email']) ?></strong> (<?= $comentario['fecha'] ?>):<br>
                <?= nl2br(htmlspecialchars($comentario['texto'])) ?>
            </li>
        <?php endforeach; ?>
    </ul>
<?php else: ?>
    <p>No hay comentarios aún.</p>
<?php endif; ?>

<?php if (isset($_SESSION['id'])): ?>
    <form action="procesar/procesar_comentario.php" method="post" novalidate>
        <input type="hidden" name="sala_id" value="<?= $id ?>">
        <textarea name="texto" required placeholder="Escribe un comentario..."></textarea><br>
        <button type="submit" class="boton">Enviar comentario</button>
    </form>
<?php else: ?>
    <p>Debes <a href="index.php?page=login">iniciar sesión</a> para comentar.</p>
<?php endif; ?>