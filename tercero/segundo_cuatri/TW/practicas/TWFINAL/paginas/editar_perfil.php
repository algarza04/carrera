<?php
require_once 'config/funciones.php';
iniciar_sesion();

$pdo = obtener_pdo();

// Obtener el ID del usuario logueado
$usuario_logueado_id = $_SESSION['id'] ?? null;

// Obtener el rol del usuario logueado
$usuario_logueado_rol = $_SESSION['rol'] ?? null;

// Obtener el ID del usuario a editar
$id = $_GET['id'] ?? $usuario_logueado_id; // Si no se pasa un ID, usar el del usuario logueado
if (!$id || !is_numeric($id)) {
    header("Location: index.php?page=listar_usuarios&error=id_invalido");
    exit;
}

if ($usuario_logueado_rol !== 'admin' && $usuario_logueado_id != $id) {
    header("Location: index.php?page=inicio&error=permiso_denegado");
    exit;
}

$stmt = $pdo->prepare("SELECT nombre, apellidos, email, dni, rol FROM usuarios WHERE id = ?");
$stmt->execute([$id]);
$usuario = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$usuario) {
    header("Location: index.php?page=listar_usuarios&error=id_invalido");
    exit;
}

$errores = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $clave = $_POST['clave'] ?? '';
    $clave_repetida = $_POST['clave_repetida'] ?? '';

    // Validar los datos
    if (empty($email)) {
        $errores['email'] = 'El email es obligatorio.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errores['email'] = 'El email no es válido.';
    } else {
        // Comprobar si el email ya existe en otro usuario
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM usuarios WHERE email = ? AND id != ?");
        $stmt->execute([$email, $id]);
        if ($stmt->fetchColumn() > 0) {
            $errores['email'] = 'El email ya está en uso.';
        }
    }

    if (!empty($clave) && strlen($clave) < 4) {
        $errores['clave'] = 'La contraseña debe tener al menos 4 caracteres.';
    }

    if (!empty($clave) && $clave !== $clave_repetida) {
        $errores['clave_repetida'] = "Las contraseñas no coinciden";
    }

    if (empty($errores)) {
        try {
            if ($usuario_logueado_rol === 'admin') {
                // Actualizar todos los campos si es administrador
                $nombre = $_POST['nombre'] ?? '';
                $apellidos = $_POST['apellidos'] ?? '';
                $dni = $_POST['dni'] ?? '';
                $rol = $_POST['rol'] ?? '';

                // Impedir que un admin se quite el admin a sí mismo
                if ($usuario_logueado_id == $id && $rol !== 'admin') {
                    $errores['rol'] = 'No puedes quitarte el rol de administrador a ti mismo.';
                } else {
                    $stmt = $pdo->prepare("UPDATE usuarios SET nombre = ?, apellidos = ?, email = ?, dni = ?, rol = ? WHERE id = ?");
                    $stmt->execute([$nombre, $apellidos, $email, $dni, $rol, $id]);
                }
            } else {
                // Actualizar solo email y contraseña si es usuario normal
                if (!empty($clave)) {
                    $clave_hash = password_hash($clave, PASSWORD_DEFAULT);
                    $stmt = $pdo->prepare("UPDATE usuarios SET email = ?, clave = ? WHERE id = ?");
                    $stmt->execute([$email, $clave_hash, $id]);
                } else {
                    $stmt = $pdo->prepare("UPDATE usuarios SET email = ? WHERE id = ?");
                    $stmt->execute([$email, $id]);
                }
            } 

            if (empty($errores)) {
                if ($usuario_logueado_id == $id) {
                    $_SESSION['email'] = $email;
                }
                if (es_admin()) {
                    header("Location: index.php?page=listar_usuarios&ok=perfil_actualizado");
                } else {
                    header("Location: index.php?page=perfil&ok=perfil_actualizado");
                }
                exit;
            }
        } catch (PDOException $e) {
            echo "<p style='color:red;'>Error al actualizar los datos: " . htmlspecialchars($e->getMessage()) . "</p>";
        }
    }
}
?>

<h2>Editar Perfil de usuario</h2>
<form action="index.php?page=editar_perfil&id=<?= $id ?>" method="post" novalidate>
    <?php if ($usuario_logueado_rol === 'admin'): ?>
        <label>Nombre:
            <input type="text" name="nombre" value="<?= htmlspecialchars($_POST['nombre'] ?? $usuario['nombre']) ?>" required>
            <?php if (!empty($errores['nombre'])): ?>
                <span style="color:red;"><?= htmlspecialchars($errores['nombre']) ?></span>
            <?php endif; ?>
        </label>
        
        <label>Apellidos:
            <input type="text" name="apellidos" value="<?= htmlspecialchars($_POST['apellidos'] ?? $usuario['apellidos']) ?>" required>
            <?php if (!empty($errores['apellidos'])): ?>
                <span style="color:red;"><?= htmlspecialchars($errores['apellidos']) ?></span>
            <?php endif; ?>
        </label>
        
        <label>DNI:
            <input type="text" name="dni" value="<?= htmlspecialchars($_POST['dni'] ?? $usuario['dni']) ?>" required>
            <?php if (!empty($errores['dni'])): ?>
                <span style="color:red;"><?= htmlspecialchars($errores['dni']) ?></span>
            <?php endif; ?>
        </label>
        
        <label>Rol:
            <select name="rol" required>
                <option value="cliente" <?= ($_POST['rol'] ?? $usuario['rol']) === 'cliente' ? 'selected' : '' ?>>Cliente</option>
                <option value="admin" <?= ($_POST['rol'] ?? $usuario['rol']) === 'admin' ? 'selected' : '' ?>>Administrador</option>
            </select>
            <?php if (!empty($errores['rol'])): ?>
                <span style="color:red;"><?= htmlspecialchars($errores['rol']) ?></span>
            <?php endif; ?>
        </label>
        
    <?php else: ?>
        <label>Nombre:
            <input type="text" value="<?= htmlspecialchars($usuario['nombre']) ?>" disabled>
        </label>
        
        <label>Apellidos:
            <input type="text" value="<?= htmlspecialchars($usuario['apellidos']) ?>" disabled>
        </label>
        
        <label>DNI:
            <input type="text" value="<?= htmlspecialchars($usuario['dni']) ?>" disabled>
        </label>
        
        <label>Rol:
            <input type="text" value="<?= htmlspecialchars($usuario['rol']) ?>" disabled>
        </label>
        
    <?php endif; ?>

    <label>Email:
        <input type="email" name="email" value="<?= htmlspecialchars($_POST['email'] ?? $usuario['email']) ?>" required>
        <?php if (!empty($errores['email'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['email']) ?></span>
        <?php endif; ?>
    </label>
    

    <label>Contraseña:
        <input type="password" name="clave" placeholder="Nueva contraseña (opcional)">
        <?php if (!empty($errores['clave'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['clave']) ?></span>
        <?php endif; ?>
    </label>
    <label>Repita contraseña:
        <input type="password" name="clave_repetida" maxlength="8" size="12" placeholder="Repita la clave">
        <?php if (!empty($errores['clave_repetida'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['clave_repetida']) ?></span>
        <?php endif; ?>
    </label>
    <button type="submit" class="boton">Guardar cambios</button>
</form>
<a href="index.php?page=inicio">Cancelar</a>