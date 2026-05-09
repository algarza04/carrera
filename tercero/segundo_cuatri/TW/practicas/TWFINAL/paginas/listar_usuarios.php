<?php

/**
 * Página para listar los usuarios del sistema
 * Solo accesible por administradores.
 * Muestra un listado con los datos básicos de cada usuario.
 * Permite editar y eliminar usuarios (el administrador actual no deja borrarlo).
 */
require_once 'config/funciones.php';
iniciar_sesion();

// Verificar si el usuario es administrador
if (!es_admin()) {
    header("Location: ../index.php?page=inicio&error=permiso");
    exit;
}

$pdo = obtener_pdo();

// Obtener todos los usuarios del sistema
$stmt = $pdo->query("SELECT id, nombre, apellidos, email, dni, rol FROM usuarios ORDER BY nombre ASC");
$usuarios = $stmt->fetchAll(PDO::FETCH_ASSOC);
$id_usuario_actual = $_SESSION['id'];

?>

<h2>Listado de Usuarios</h2>
<?php foreach ($usuarios as $usuario): ?>
<div class="usuario">
    <img src="../imagenes/hombre1.jpg" alt="Foto de usuario" style="width:100px; height:auto; border-radius:50%;">
    <div>
        <p><strong>Nombre:</strong> <?= htmlspecialchars($usuario['nombre']) ?></p>
        <p><strong>Apellidos:</strong> <?= htmlspecialchars($usuario['apellidos']) ?></p>
        <p><strong>Email:</strong> <?= htmlspecialchars($usuario['email']) ?></p>
        <p><strong>DNI:</strong> <?= htmlspecialchars($usuario['dni']) ?></p>
        <p><strong>Tipo de usuario:</strong> <?= $usuario['rol'] === 'admin' ? 'Administrador' : 'Cliente' ?></p>
    </div>
    <div>
        <button class="editar" onclick="window.location.href='index.php?page=editar_perfil&id=<?=$usuario['id'] ?>'">Editar</button>
        <?php if ($usuario['id'] !== $id_usuario_actual): ?>
            <button class="borrar" onclick="if(confirm('¿Estás seguro de que deseas borrar este usuario?')) window.location.href='procesar/eliminar_usuario.php?id=<?= $usuario['id'] ?>'">Borrar</button>
        <?php else: ?>
            <button class="borrar" disabled style="background-color: gray; cursor: not-allowed;">No puedes borrarte a ti mismo</button>
        <?php endif; ?>    </div>
</div>
<?php endforeach; ?>