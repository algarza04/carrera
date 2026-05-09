<?php
/**
 * Pagina para realizar reservas de salas
 * Permite seleccionar una fecha, avanzar/retroceder días o meses  yseleccionar una fecha.
 * Una vez seleccionada permite reservar una sala en un horario concreto.   
 */
require_once 'config/funciones.php';
iniciar_sesion();

$fecha = $_GET['fecha'] ?? date('Y-m-d');
$es_admin = es_admin();
// Lógica para avanzar/retroceder día o mes
if (isset($_GET['accion'])) {
    switch ($_GET['accion']) {
        case 'hoy':
            $fecha = date('Y-m-d');
            break;
        case 'avanzar_dia':
            $fecha = date('Y-m-d', strtotime("$fecha +1 day"));
            break;
        case 'retroceder_dia':
            $fecha = date('Y-m-d', strtotime("$fecha -1 day"));
            break;
        case 'avanzar_mes':
            $fecha = date('Y-m-d', strtotime("$fecha +1 month"));
            break;
        case 'retroceder_mes':
            $fecha = date('Y-m-d', strtotime("$fecha -1 month"));
            break;
    }
}
?>

<div>
    <form method="get" action="index.php" novalidate>
        <input type="hidden" name="page" value="reservas">
        <input type="hidden" name="fecha" value="<?= $fecha ?>">
        <button name="accion" value="hoy">Hoy</button>
        <button name="accion" value="retroceder_dia">Retroceder día</button>
        <button name="accion" value="avanzar_dia">Avanzar día</button>
        <button name="accion" value="retroceder_mes">Retroceder mes</button>
        <button name="accion" value="avanzar_mes">Avanzar mes</button>
        <button type="submit" name="aceptar_fecha" value="1" style="background: #4CAF50; color: white;">Aceptar fecha</button>
    </form>
    <h2>Fecha seleccionada: <?= date('d/m/Y', strtotime($fecha)) ?></h2>
</div>
<?php
if (isset($_GET['fecha'])) {
    $fecha_actual = $_GET['fecha'];
} else {
    $fecha_actual = date('Y-m-d');
}
$mes = date('m', strtotime($fecha_actual));
$anio = date('Y', strtotime($fecha_actual));

$primer_dia = date('N', strtotime("$anio-$mes-01")); // 1 (lunes) - 7 (domingo)
$dias_mes = date('t', strtotime("$anio-$mes-01"));

$meses = [
    1 => "Enero", 2 => "Febrero", 3 => "Marzo", 4 => "Abril",
    5 => "Mayo", 6 => "Junio", 7 => "Julio", 8 => "Agosto",
    9 => "Septiembre", 10 => "Octubre", 11 => "Noviembre", 12 => "Diciembre"
];
?>
<div style="display:inline-block; vertical-align:top; margin-left:30px;">
    <table style="border-collapse:collapse; text-align:center; color: white">
        <tr>
            <th colspan="7" style="background:#e3f2fd;">
                <a href="index.php?page=reservas&fecha=<?=date('Y-m-d', strtotime("$anio-$mes-01 -1 month"))?>&aceptar_fecha=1" style="text-decoration:none;">&#9664;</a>
                <?= $meses[intval($mes)] . " $anio" ?>
                <a href="index.php?page=reservas&fecha=<?=date('Y-m-d', strtotime("$anio-$mes-01 +1 month"))?>&aceptar_fecha=1" style="text-decoration:none;">&#9654;</a>
            </th>
        </tr>
        <tr style="background:#90caf9;">
            <th>L</th><th>M</th><th>M</th><th>J</th><th>V</th><th>S</th><th>D</th>
        </tr>
        <tr style='background:white;'>
        <?php
        $dia = 1;
        // Espacios en blanco hasta el primer día
        for ($i = 1; $i < $primer_dia; $i++) {
            echo "<td></td>";
        }
        for ($i = $primer_dia; $i <= 7; $i++) {
            $fecha_dia = sprintf('%04d-%02d-%02d', $anio, $mes, $dia);
            $estilo = ($fecha_dia == $fecha_actual) ? 'background:#a5d6a7;' : '';
            echo "<td style='$estilo'><a href='index.php?page=reservas&fecha=$fecha_dia&aceptar_fecha=1' style='text-decoration:none;color:black;'>$dia</a></td>";
            $dia++;
        }
        echo "</tr>";
        // Resto de semanas
        while ($dia <= $dias_mes) {
            echo "<tr style='background:white;'>";
            for ($i = 1; $i <= 7; $i++) {
                if ($dia > $dias_mes) {
                    echo "<td></td>";
                } else {
                    $fecha_dia = sprintf('%04d-%02d-%02d', $anio, $mes, $dia);
                    $estilo = ($fecha_dia == $fecha_actual) ? 'background:#a5d6a7;' : '';
                    echo "<td style='$estilo'><a href='index.php?page=reservas&fecha=$fecha_dia&aceptar_fecha=1' style='text-decoration:none;color:black;'>$dia</a></td>";
                    $dia++;
                }
            }
            echo "</tr>";
        }
        ?>
    </table>
</div>

<?php
if (isset($_GET['error']) && $_GET['error'] === 'solapada') {
    echo "<p style='color:red;'>¡Ya existe una reserva en ese horario!</p>";
}
if (isset($_GET['ok'])) {
    echo "<p style='color:green;'>Reserva realizada correctamente.</p>";
}

if (isset($_GET['aceptar_fecha'])) {
    $pdo = obtener_pdo();

    $stmt = $pdo->query("SELECT hora_apertura, hora_cierre FROM configuracion_centro LIMIT 1");
    $config = $stmt->fetch(PDO::FETCH_ASSOC);
    $hora_inicio = strtotime($config['hora_apertura']);
    $hora_fin = strtotime($config['hora_cierre']);
    $slots = [];
    while ($hora_inicio < $hora_fin) {
        $slots[] = date('H:i', $hora_inicio);
        $hora_inicio = strtotime('+1 hour', $hora_inicio);
    }

    // Obtener salas
    $stmt = $pdo->query("SELECT * FROM salas");
    $salas = $stmt->fetchAll();

    // Obtener reservas de ese día
    $stmt = $pdo->prepare("SELECT r.*, u.email FROM reservas r JOIN usuarios u ON r.usuario_id = u.id WHERE r.fecha = ?");
    $stmt->execute([$fecha]);
    $reservas = $stmt->fetchAll();

    // Indexar reservas por sala y slot
    $reserva_map = [];
    foreach ($reservas as $res) {
        $start = strtotime($res['hora_inicio']);
        $end = strtotime($res['hora_fin']);
        foreach ($slots as $slot) {
            $slot_time = strtotime($slot);
            if ($slot_time >= $start && $slot_time < $end) {
                $reserva_map[$res['sala_id']][$slot] = $res;
            }
        }
    }

    echo "<h2>Reservas para el " . date('d/m/Y', strtotime($fecha)) . "</h2>";
    echo "<table style='border-collapse:collapse; width:100%; margin-top:15px; font-size:0.8em;'>";
    echo "<tr><th>Salas</th>";
    foreach ($slots as $slot) {
        echo "<th>$slot</th>";
    }
    echo "</tr>";

    foreach ($salas as $sala) {
    // Fondo gris si no es reservable
    $row_style = $sala['reservable'] ? '' : 'style="background:#eee"';
    echo "<tr $row_style>";
    echo "<td><a href='index.php?page=sala&id={$sala['id']}' title='Ver sala'>" . htmlspecialchars($sala['nombre']) . "</a></td>";
        foreach ($slots as $slot) {
        if (isset($reserva_map[$sala['id']][$slot])) {
            $res = $reserva_map[$sala['id']][$slot];
            $es_admin = isset($_SESSION['rol']) && $_SESSION['rol'] === 'admin';
            $info = htmlspecialchars($res['motivo']);
            if ($es_admin) {
                $info .= " (" . htmlspecialchars($res['email']) . ")";
            }
            if ($res['usuario_id'] == $_SESSION['id']) {
                // Reserva propia: verde + botón cancelar
                echo "<td style='background:#b6fcb6;' title='$info'>
                        $info
                        <form method='post' novalidate action='procesar/cancelar_reserva.php' style='margin:0;display:inline'>
                            <input type='hidden' name='reserva_id' value='{$res['id']}'>
                            <input type='hidden' name='fecha' value='$fecha'>
                            <button type='submit' style='padding:0 4px; color:red;'>Cancelar</button>
                        </form>
                    </td>";
            } elseif ($es_admin) {
                // Reserva de otro usuario, pero admin: naranja + botón cancelar
                echo "<td style='background:#b6d4fc;' title='$info'>
                        $info
                        <form method='post' novalidate action='procesar/cancelar_reserva.php' style='margin:0;display:inline'>
                            <input type='hidden' name='reserva_id' value='{$res['id']}'>
                            <input type='hidden' name='fecha' value='$fecha'>
                            <button type='submit' style='padding:0 4px; color:red;'>Cancelar</button>
                        </form>
                    </td>";
            } else {
                // Reserva de otro usuario: azul
                echo "<td style='background:#b6d4fc;' title='$info'>$info</td>";
            }
        } else {
            // No hay reserva
            if (!$sala['reservable'] && !$es_admin) {
                // No reservable y no admin: celda gris
                echo "<td style='background:#eee'></td>";
            } else {
                // Reservable o admin: formulario de reserva rápida
                echo "<td>
                    <form method='post' novalidate action='procesar/procesar_reservas.php' style='margin:0'>
                        <input type='hidden' name='sala_id' value='{$sala['id']}'>
                        <input type='hidden' name='fecha' value='$fecha'>
                        <input type='hidden' name='hora_inicio' value='$slot'>
                        <input type='hidden' name='hora_fin' value='" . date('H:i', strtotime("$slot +1 hour")) . "'>
                        <input type='text' name='motivo' placeholder='Motivo' style='width:60px' required>
                        <button type='submit' style='padding:0 4px;'>Reservar</button>
                    </form>
                </td>";
            }
        }
    }
    echo "</tr>";
}

    echo "</table>";
}
?>