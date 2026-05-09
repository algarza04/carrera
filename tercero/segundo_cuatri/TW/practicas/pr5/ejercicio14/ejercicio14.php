<?php
session_start();

if (!isset($_SESSION['tablero']) || isset($_POST['limpiar'])) {
    $_SESSION['tablero'] = array_fill(0, 3, array_fill(0, 3, ''));
    $_SESSION['turno'] = 'rojo';
    $_SESSION['ganador'] = null;
    $_SESSION['tres_en_raya'] = null;
}

if (!isset($_SESSION['ganador'])) {
    foreach ($_POST as $key => $value) {
        if (preg_match('/poner(\d)(\d)/', $key, $matches)) {
            $i = $matches[1];
            $j = $matches[2];
            if ($_SESSION['tablero'][$i][$j] === '') {
                $_SESSION['tablero'][$i][$j] = $_SESSION['turno'];
                comprobarGanador();
                $_SESSION['turno'] = $_SESSION['turno'] === 'rojo' ? 'azul' : 'rojo';
            }
            break;
        }
    }
}

function comprobarGanador() {
    $t = $_SESSION['tablero'];
    $lineas = [];

    for ($i = 0; $i < 3; $i++) {
        $lineas[] = [[$i,0], [$i,1], [$i,2]];
        $lineas[] = [[0,$i], [1,$i], [2,$i]];
    }
    $lineas[] = [[0,0], [1,1], [2,2]];
    $lineas[] = [[0,2], [1,1], [2,0]];

    foreach ($lineas as $linea) {
        [$a, $b, $c] = $linea;
        $v1 = $_SESSION['tablero'][$a[0]][$a[1]];
        $v2 = $_SESSION['tablero'][$b[0]][$b[1]];
        $v3 = $_SESSION['tablero'][$c[0]][$c[1]];
        if ($v1 !== '' && $v1 === $v2 && $v2 === $v3) {
            $_SESSION['ganador'] = $v1;
            $_SESSION['tres_en_raya'] = $linea;
            return;
        }
    }

    $empate = true;
    foreach ($t as $fila) {
        foreach ($fila as $celda) {
            if ($celda === '') {
                $empate = false;
                break 2;
            }
        }
    }
    if ($empate) {
        $_SESSION['ganador'] = 'empate';
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ejercicio 14</title>
    <style>
        body {
            font-family: helvetica;
        }
        .juego {
            width: 250px;
            margin: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .juego > h1 {
            width: 100%;
            background-color: lightgreen;
            text-align: center;
        }
        .juego > .informacion {
            width: 100%;
            background-color: lightgreen;
            margin: 5px 0;
            padding: 5px;
            text-align: center;
        }
        .informacion img {
            vertical-align: middle;
        }
        .libre {
            transition: transform .5s ease-in-out;
        }
        .libre:hover {
            transform: scale(1.5);
            cursor: pointer;
        }
        .ganador {
            animation: anim 0.5s infinite linear alternate;
        }
        @keyframes anim {
            from {transform: scale(1);}
            to {transform: scale(1.5);}
        }
        table {
            border-spacing: 5px;
        }
    </style>
</head>
<body>
<section class="juego">
    <h1>3 en raya</h1>

    <section class="tablero">
        <form method="post" action="">
            <table>
                <?php
                for ($i = 0; $i < 3; $i++) {
                echo '<tr>';
                    for ($j = 0; $j < 3; $j++) {
                        $turno = $_SESSION['tablero'][$i][$j];
                        if ($turno == 'rojo') 
                            $img = "imagenes/brojo.png";
                        else if ($turno == 'azul')
                            $img = "imagenes/bazul.png";
                        else
                            $img = "imagenes/bamarillo.png";
                        
                        $nombre = "poner{$i}{$j}";
                        $clase = ($turno === '') ? 'libre' : '';

                        if (isset($_SESSION['tres_en_raya'])) {
                            foreach ($_SESSION['tres_en_raya'] as $posicion) {
                                if ($posicion[0] === $i && $posicion[1] === $j) {
                                    $clase .= ' ganador';
                                    break;
                                }
                            }
                        }
                    ?>
                    <td><input type="image" class="<?= $clase ?>" src="<?= $img ?>" width="50px" formmethod="post" name="<?= $nombre ?>"></td>
                    <?php } ?>

                </tr>
                <?php } ?>      
            </table>
        </form>
    </section>

    <section class="informacion">
        <?php if (isset($_SESSION['ganador'])): ?>
            <?php if ($_SESSION['ganador'] === 'empate'): ?>
                <p>¡Empate!</p>
            <?php else: ?>
                <p>Ha ganado: <img src="imagenes/b<?= $_SESSION['ganador'] ?>.png" width="25"></p>
            <?php endif; ?>
        <?php else: ?>
            <p>Turno: <img src="imagenes/b<?= $_SESSION['turno'] ?>.png" width="25"></p>
        <?php endif; ?>
    </section>

    <section class="botones">
        <form method="post" action="">
            <input type="submit" name="limpiar" value="Limpiar">
        </form>
    </section>
</section>
</body>
</html>
