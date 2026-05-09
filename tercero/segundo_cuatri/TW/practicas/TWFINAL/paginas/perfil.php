<?php
/**
 * Pagina para mostrar el perfil del usuario
 * Muestra los datos del usuario logueado: nombre, apellidos, dni, email y fotografía.
 * Permite editar el perfil.
 */
require_once 'config/funciones.php';
iniciar_sesion();
mandar_a_login();

$pdo = obtener_pdo();

// Obtener los datos del usuario desde la base de datos
$stmt = $pdo->prepare("SELECT nombre, apellidos, dni, email FROM usuarios WHERE id = ?");
$stmt->execute([$_SESSION['id']]);
$usuario = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$usuario) {
    echo "<p style='color:red;'>Error: No se pudieron cargar los datos del usuario.</p>";
    exit;
}
?>

<h2>Perfil de Usuario</h2>
<div style="border:1px solid #ccc; padding:10px; border-radius:8px; max-width:400px;">
    <p><strong>Nombre:</strong> <?= htmlspecialchars($usuario['nombre']) ?></p>
    <p><strong>Apellidos:</strong> <?= htmlspecialchars($usuario['apellidos']) ?></p>
    <p><strong>DNI:</strong> <?= htmlspecialchars($usuario['dni']) ?></p>
    <p><strong>Email:</strong> <?= htmlspecialchars($usuario['email']) ?></p>
    <p><strong>Fotografía:</strong></p>
    <?php if (!empty($foto)): ?>
        <img src="<?= htmlspecialchars($foto) ?>" alt="Foto de perfil" style="width:150px; height:auto; border-radius:50%;">
    <?php else: ?>
        <img src="imagenes/imagen_perfil.png" alt="Foto por defecto" style="width:150px; height:auto; border-radius:50%;">
    <?php endif; ?>
</div>

<p><a href="index.php?page=editar_perfil" class="boton" style="text-decoration:none;">Editar Perfil</a></p>

<?php if (isset($_GET['ok']) && $_GET['ok'] === 'perfil_actualizado'): ?>
    <p style="color:green;">¡Perfil actualizado correctamente!</p>
<?php endif; ?>