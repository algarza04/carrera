<?php
/**
 * Página para crear un nuevo usuario
 * Permite a los administradores crear usuarios y a los clientes registrarse.
 * Muestra un formulario con los campos necesarios y valida los datos.
 * Si se envían datos incorrectos, muestra los errores.
 * Si se confirma el registro, deshabilita los campos para evitar cambios.
 */
$errores = isset($_GET['errores']) ? json_decode(urldecode($_GET['errores']), true) : [];
$datos = isset($_GET['datos']) ? json_decode(urldecode($_GET['datos']), true) : [
    'nombre' => '',
    'apellidos' => '',
    'dni' => '',
    'email' => '',
    'clave' => '',
    'clave_repetida' => '',
    'rol' => ''
];

$deshabilitado = isset($_GET['confirmar']) && $_GET['confirmar'] == 1;

$es_admin = es_admin();
?>

<h2><?= $es_admin ? 'Crear usuario' : 'Registro de usuario' ?></h2>
<form action="procesar/procesar_registro.php" method="post" novalidate enctype="multipart/form-data">
    <label>Nombre:
        <input type="text" name="nombre" size="20" placeholder="El nombre es obligatorio" required
            value="<?= htmlspecialchars($datos['nombre'] ?? '') ?>" <?= $deshabilitado ? 'readonly' : '' ?>>
        <?php if ($deshabilitado): ?>
            <input type="hidden" name="nombre" value="<?= htmlspecialchars($datos['nombre'] ?? '') ?>">
        <?php endif; ?>
        <?php if (!$deshabilitado && !empty($errores['nombre'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['nombre']) ?></span>
        <?php endif; ?>
    </label>

    <label>Apellidos:
        <input type="text" name="apellidos" size="30" placeholder="El apellido es obligatorio" required
            value="<?= htmlspecialchars($datos['apellidos'] ?? '') ?>" <?= $deshabilitado ? 'readonly' : '' ?>>
        <?php if ($deshabilitado): ?>
            <input type="hidden" name="apellidos" value="<?= htmlspecialchars($datos['apellidos'] ?? '') ?>">
        <?php endif; ?>
        <?php if (!$deshabilitado && !empty($errores['apellidos'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['apellidos']) ?></span>
        <?php endif; ?>
    </label>

    <label>DNI:
        <input type="text" name="dni" size="10" placeholder="Ej: 12345678Z" required
            value="<?= htmlspecialchars($datos['dni'] ?? '') ?>" <?= $deshabilitado ? 'readonly' : '' ?>>
        <?php if ($deshabilitado): ?>
            <input type="hidden" name="dni" value="<?= htmlspecialchars($datos['dni'] ?? '') ?>">
        <?php endif; ?>
        <?php if (!$deshabilitado && !empty($errores['dni'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['dni']) ?></span>
        <?php endif; ?>
    </label>

    <label>E-mail:
        <input type="email" name="email" size="30" placeholder="e-mail obligatorio" required
            value="<?= htmlspecialchars($datos['email'] ?? '') ?>" <?= $deshabilitado ? 'readonly' : '' ?>>
        <?php if ($deshabilitado): ?>
            <input type="hidden" name="email" value="<?= htmlspecialchars($datos['email'] ?? '') ?>">
        <?php endif; ?>
        <?php if (!$deshabilitado && !empty($errores['email'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['email']) ?></span>
        <?php endif; ?>
    </label>

    <label>Fotografía
        <input disabled type="file" name="foto" <?= $deshabilitado ? 'disabled' : '' ?>>
        <!-- No se puede enviar el archivo como hidden, solo se muestra deshabilitado -->
    </label>

    <label>Contraseña:
        <input type="password" name="clave" maxlength="8" size="12" required placeholder="Escriba la clave"
            value="<?= htmlspecialchars($datos['clave'] ?? '') ?>" <?= $deshabilitado ? 'readonly' : '' ?>>
        <?php if ($deshabilitado): ?>
            <input type="hidden" name="clave" value="<?= htmlspecialchars($datos['clave'] ?? '') ?>">
        <?php endif; ?>
        <?php if (!$deshabilitado && !empty($errores['clave'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['clave']) ?></span>
        <?php endif; ?>
    </label>

    <label>Repita contraseña:
        <input type="password" name="clave_repetida" maxlength="8" size="12" required placeholder="Repita la clave"
            value="<?= htmlspecialchars($datos['clave_repetida'] ?? '') ?>" <?= $deshabilitado ? 'readonly' : '' ?>>
        <?php if ($deshabilitado): ?>
            <input type="hidden" name="clave_repetida" value="<?= htmlspecialchars($datos['clave_repetida'] ?? '') ?>">
        <?php endif; ?>
        <?php if (!$deshabilitado && !empty($errores['clave_repetida'])): ?>
            <span style="color:red;"><?= htmlspecialchars($errores['clave_repetida']) ?></span>
        <?php endif; ?>
    </label>

    <?php if ($es_admin): ?>
        <label>Rol:
            <select name="rol" required <?= $deshabilitado ? 'disabled' : '' ?>>
                <option value="cliente" <?= ($datos['rol'] ?? '') === 'cliente' ? 'selected' : '' ?>>Cliente</option>
                <option value="admin" <?= ($datos['rol'] ?? '') === 'admin' ? 'selected' : '' ?>>Administrador</option>
            </select>
            <?php if ($deshabilitado): ?>
                <input type="hidden" name="rol" value="<?= htmlspecialchars($datos['rol'] ?? '') ?>">
            <?php endif; ?>
            <?php if (!$deshabilitado && !empty($errores['rol'])): ?>
                <span style="color:red;"><?= htmlspecialchars($errores['rol']) ?></span>
            <?php endif; ?>
        </label>
    <?php endif; ?>

    <div>
    <?php if ($deshabilitado): ?>
        <button class="boton" type="submit" name="envio_final" value="1">Aceptar</button>
        <a class="boton" style="text-decoration: none;"href="index.php?page=registro&<?= http_build_query(['datos'=>json_encode($datos)]) ?>">Cancelar</a>
    <?php else: ?>
        <input class="boton" type="submit" value="Enviar datos" name="envio">
        <input class="boton" type="reset" value="Borrar formulario" name="borrar">  
    <?php endif; ?>
    </div>
</form>