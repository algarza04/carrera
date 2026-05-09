<?php
/**
 * Pagina para que los usuarios inicien sesión
 * Permite introducir email y contraseña.
 * Si hay errores, se muestran en rojo.
 */
// Recoger errores y datos si vienen por GET (codificados en JSON)
$error = isset($_GET['error']) ? json_decode(urldecode($_GET['error']), true) : [];
$datos = isset($_GET['datos']) ? json_decode(urldecode($_GET['datos']), true) : [
    'email' => '',
    'clave' => ''
];
?>

<h2>Login de usuario</h2>
<form action="procesar/procesar_login.php" method="post" novalidate>
    <label>E-mail:
        <input type="email" name="email" size="20" placeholder="e-mail obligatorio" required
            value="<?= htmlspecialchars($datos['email'] ?? '') ?>">
    </label>

    <label>Contraseña:
        <input type="password" name="clave" maxlength="8" size="12" required placeholder="Escriba la clave">
    </label>

    <p>
    <?php if ($error != null): ?>
        <span style="color:red;"><?= htmlspecialchars($error) ?></span>
    <?php endif; ?>
    </p>

    <fieldset>
        <input type="submit" name="inicio" value="Iniciar sesión">
    </fieldset>
</form>
