<?php
function calcular_imc($peso, $altura_cm) {
    $altura_m = $altura_cm / 100;
    return round($peso / ($altura_m * $altura_m), 2);
}
function categoria_imc($imc) {
    if ($imc < 18.5) return "Bajo peso";
    if ($imc < 25)   return "Normal";
    if ($imc < 30)   return "Sobrepeso";
    return "Obesidad";
}

$imc = $categoria = null;
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $peso = floatval($_POST["peso"]);
    $altura = floatval($_POST["altura"]);
    $imc = calcular_imc($peso, $altura);
    $categoria = categoria_imc($imc);
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Calculadora IMC</title>
</head>
<body>
    <?php if ($imc !== null): ?>
    <h1>Tu IMC es <?= $imc ?></h1>
    <p>
        Categoría: <strong><?= $categoria ?></strong>
    </p>
    <?php else: ?>
    <h1>Ingrese sus datos</h1>
    <form method="post">
        <label>Peso (kg): <input name="peso" type="number" step="0.1" required></label>
        <label>Altura (cm): <input name="altura" type="number" required></label>
        <button type="submit">Calcular IMC</button>
    </form>
    <?php endif; ?>
</body>
</html>