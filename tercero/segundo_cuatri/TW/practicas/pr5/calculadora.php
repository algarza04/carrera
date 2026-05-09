<?php
    $dato1 = '';
    $dato2 = '';
    $error = [];
    $operacion = '';
    $result = '';
    
    if($dato1 != null)
        $numero1 = $dato1;
    if($dato2 != null)
        $numero2 = $dato2;

    if (isset($_GET['suma'])) {
        if (is_numeric($_GET['numero1']) && is_numeric($_GET['numero2'])) {
            $result = $_GET['numero1'] + $_GET['numero2'];
            $operacion = 'suma';
        } else {
            if (!is_numeric($_GET['numero1'])) {
                $error[] = "ERROR: El primer dato no es válido";
            }
            else {
                $dato1 = $_GET['numero1'];
            }
            if (!is_numeric($_GET['numero2'])) {
                $error[] = "ERROR: El segundo dato no es válido";
            }
            else {
                $dato2 = $_GET['numero2'];
            }
        }
    } elseif (isset($_GET['resta'])) {
        if (is_numeric($_GET['numero1']) && is_numeric($_GET['numero2'])) {
            $result = $_GET['numero1'] - $_GET['numero2'];
            $operacion = 'resta';
        } else {
            if (!is_numeric($_GET['numero1'])) {
                $error[] = "ERROR: El primer dato no es válido";
            }
            else {
                $dato1 = $_GET['numero1'];
            }
            if (!is_numeric($_GET['numero2'])) {
                $error[] = "ERROR: El segundo dato no es válido";
            } else {
                $dato2 = $_GET['numero2'];
            }
        }
    } elseif (isset($_GET['producto'])) {
        if (is_numeric($_GET['numero1']) && is_numeric($_GET['numero2'])) {
            $result = $_GET['numero1'] * $_GET['numero2'];
            $operacion = 'producto';
        } else {
            if (!is_numeric($_GET['numero1'])) {
                $error[] = "ERROR: El primer dato no es válido";
            } else {
                $dato1 = $_GET['numero1'];
            }
            if (!is_numeric($_GET['numero2'])) {
                $error[] = "ERROR: El segundo dato no es válido";
            } else {
                $dato2 = $_GET['numero2'];
            }
        }
    } elseif (isset($_GET['division'])) {
        if (is_numeric($_GET['numero1']) && is_numeric($_GET['numero2'])) {
            if ($_GET['numero2'] == 0) {
                $error[] = "ERROR: División por cero";
                $dato1 = $_GET['numero1'];
            } else {
                $result = $_GET['numero1'] / $_GET['numero2'];
                $operacion = 'division';
            }
        } else {
            if (!is_numeric($_GET['numero1'])) {
                $error[] = "ERROR: El primer dato no es válido";
            }
            else {
                $dato1 = $_GET['numero1'];
            }
            if (!is_numeric($_GET['numero2'])) {
                $error[] = "ERROR: El segundo dato no es válido";
            } elseif($_GET['numero2'] != 0){ 
                $dato2 = $_GET['numero2'];
            }
        }
    }else {
        echo "No se ha realizado ninguna operación";
    }
echo <<<HTML
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Calculadora</title>
        <style>
            main {
                font-family: Arial;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            form {
                border: 2px solid lightgray;
                padding: 5px;
                display: inline-flex;
                align-items: center;
                background-color: lightblue;
            }
            fieldset {
                display: flex;
                flex-direction: column;
            }
            label {
                margin: 10px;
                display: flex;
                flex-direction: column;
            }
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <main>
            <h1>Calculadora</h1>
            <form action="" method="GET">
                <label><span>Dato 1</span><input type="text" name="numero1" placeholder="Introduce un número" value="${dato1}"/></label>
                <fieldset>
                    <legend>Operación</legend>
                    <input type="submit" name="suma" value="+">
                    <input type="submit" name="resta" value="-">
                    <input type="submit" name="producto" value="*">
                    <input type="submit" name="division" value="/">
                </fieldset>
                <label><span>Dato 2</span><input type="text" name="numero2" placeholder="Introduce un número" value="${dato2}"/></label>
            </form>
            <section>
HTML;
    foreach ($error as $e)
        echo '<p class="error">' . $e . '</p>';
    echo <<<HTML
                <p>Operación: <span> $operacion</span></p>
                <p>Resultado: <span> $result</span></p>
            </section>
        </main>
    </body>
    </html>
HTML;
?>