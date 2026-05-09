<?php
    $mensajes = json_decode(file_get_contents('ejercicio8.json'), true);
    
    $idioma = 'es';
    $idiomas = [
        'es' => 'Español',
        'en' => 'English',
        'fr' => 'Français'
    ];
    $caducidad = 24 * 60 * 60;  //1 día
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['idioma'])) {
        $idioma = $_POST['idioma'];
        setcookie('idioma', $idioma, time()+$caducidad);
    } elseif (isset($_COOKIE['idioma'])) {
        $idioma = $_COOKIE['idioma'];
    }

    if (!isset($mensajes[$idioma])) {
        $idioma = 'es';
    }

    $options = '';
    foreach ($idiomas as $codigo => $nombre) {  //codigo es el idioma abreviado(es, en, fr)
        $selected = $codigo === $idioma ? 'selected' : '';
        $options .= "<option value=\"$codigo\" $selected>$nombre</option>\n";
    }
    $texto = $mensajes[$idioma];

    echo <<<HTML
        <!DOCTYPE html>
        <html lang="<?php echo ($idioma); ?>">
        <head>
            <meta charset="UTF-8">
            <title>Ejercicio 8</title>
        </head>
        <body>
            <main>
                <p>${texto['Bienvenida']}</p>
                <p>${texto['Cambio']}</p>
                <form method="post">
                    <label for="idioma">${texto['ElegirIdioma']}</label>
                    <select name="idioma" id="idioma">
                        $options
                    </select>
                    <button type="submit">${texto['Aplicar']}</button>
                </form>
                <a href="">${texto['Enlace']}</a>
            </main>
        </body>
        </html>
    HTML;
?>