<?php
echo <<<HTML
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ver informacion</title>
</head>
<body>
    <h1>Información alojada en _SERVER</h1>
    <p>
HTML;

print_r($_SERVER);

echo <<<HTML
    </p>
</body>
</html>
HTML;
?>