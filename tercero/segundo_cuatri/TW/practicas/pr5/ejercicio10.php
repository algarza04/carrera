<?php
session_start();

if (isset($_POST['borrar'])) { // borrar y limpiar la sesión
    session_unset();
    session_destroy();
}

if (isset($_POST['nombre']) && $_POST['nombre'] !== '') {   // enviar
    $_SESSION['nombre'] = $_POST['nombre'];
    $_SESSION['numeros'] = [random_int(10000000, 19999999)];
} elseif (isset($_SESSION['nombre']) && !isset($_POST['nombre'])) {   // cargar de nuevo
    $_SESSION['numeros'][] = random_int(10000000, 19999999);
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ejercicio 10</title>
    <style>
        div button {
            margin: 5px;
            display: inline-block;
        }
    </style>
</head>
<body>

    <?php if (isset($_SESSION['nombre'])): ?>
        <p>Bienvenido <?= $_SESSION['nombre'] ?></p>
        <?php if (!empty($_SESSION['numeros'])): ?>
            <?php $ultimo = end($_SESSION['numeros']); //obtener ultimo numero ?>
            <ol>
                <?php foreach ($_SESSION['numeros'] as $numero): ?>
                    <?php if ($numero !== $ultimo): ?>
                        <li><?= $numero ?></li>
                    <?php endif; ?>
                <?php endforeach; ?>
            </ol>

            <p>El nuevo número es: <?= $ultimo ?></p>
        <?php endif; ?>
    <?php endif; ?>

    <form method="post" enctype="multipart/form-data">
        <label for="nombre">Dígame su nombre para comenzar:</label>
        <input type="text" name="nombre" id="nombre">
        <div>
            <button type="submit" value="Enviar">Enviar</button>
            <button type="submit" name="borrar">Borrar sesión</button>
        </div>
    </form>

    <a class="link" href="<?= $_SERVER['PHP_SELF'] ?>">Cargar de nuevo</a>
</body>
</html>