<?php
preg_match('#([^/]*php)/(.*)$#',$_SERVER['PHP_SELF'],$coincidencias);
$chunks = (count($coincidencias)>0) ? explode('/',$coincidencias[2]) : [];
if (count($chunks)>0)
    echo '<pre>' . var_export($chunks,true) . '</pre>';
else 
    echo'<p>No hay trailing path</p>';

$operacion = $chunks[0] ?? null;
$resultado = "Operación no válida o datos incorrectos.";
$mensajeError = '';

if (isset($_GET['a'])) 
    $a = (float) $_GET['a'];
else
    $a = null;

if (isset($_GET['b']))
    $b = (float) $_GET['b'];
else
    $b = null;

if ($operacion != null && is_numeric($a) && is_numeric($b)) {
    switch ($operacion) {
        case 'suma':
            $resultado = $a + $b;
            break;
        case 'resta':
            $resultado = $a - $b;
            break;
        case 'multiplica':
            $resultado = $a * $b;
            break;
        case 'divide':
            if ($b == 0)
                $mensajeError = 'No se puede dividir por cero.';
            else
                $resultado = $a / $b;
            break;
    }
} else {
    $mensajeError = 'Faltan parámetros o la operación.';
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Operar</title>
    <style>
        .mensajeError {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Resultado de la operación</h1>
    <?php if ($mensajeError): ?>
        <p><?= $mensajeError ?></p>
    <?php else: ?>
        <p><?= htmlspecialchars($operacion) ?> de <?= $a ?> y <?= $b ?> es <?= $resultado ?></p>
    <?php endif; ?>
</body>
</html>