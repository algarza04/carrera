<?php
// filepath: /home/alvarogz/Escritorio/TWFINAL/procesar/reiniciar_BBDD.php
require_once '../config/funciones.php';
iniciar_sesion();

// Verificar si el usuario es administrador
if (!es_admin()) {
    header("Location: ../index.php?page=inicio&error=permiso_denegado");
    exit;
}

$pdo = obtener_pdo();

try {
    // Desactivar las claves foráneas temporalmente
    $pdo->exec("SET FOREIGN_KEY_CHECKS = 0");


    // Vaciar las tablas en el orden correcto para evitar conflictos
    $tablas = ['comentarios', 'fotos', 'log', 'reservas', 'salas', 'configuracion_centro', 'usuarios'];
    foreach ($tablas as $tabla) {
        $pdo->exec("TRUNCATE TABLE `$tabla`");
    }

    // Reactivar las claves foráneas
    $pdo->exec("SET FOREIGN_KEY_CHECKS = 1");

    // Insertar un administrador inicial
    $clave_admin = password_hash('admin', PASSWORD_DEFAULT);
    $pdo->exec("
        INSERT INTO usuarios (nombre, apellidos, dni, email, clave, rol) VALUES
        ('admin', 'admin', '12345678Z','admin@void.ugr.es', '$clave_admin', 'admin')
    ");

    $pdo->exec("INSERT INTO configuracion_centro (nombre, logotipo, descripcion, hora_apertura, hora_cierre)
VALUES ('ETSIIT', 'imagenes/centro/log_centro.png', 'Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación (ETSIIT) es un centro docente de la Universidad de Granada situado en el campus Aynadamar,junto a la Facultad de Bellas Artes. docente.
Los grados en Ingeniería Informática e Ingeniería en Tecnologías de Telecomunicaciónde la UGR han obtenido los sellos internacionales de calidad EURO-INF y EURO-ACE respectivamente concedidos por la European Quality Assurance Network for Informatics Education (EQANIE) en el caso de EUROINF y por la European Network for the Accreditation of Engineering Education (ENAEE) en el caso de EUROACE', '08:00:00', '20:00:00')");
    registrar_evento("Base de datos reiniciada por el administrador " . $_SESSION['email']);
    
    session_destroy();

    header("Location: ../index.php?page=inicio&ok=reinicio_exitoso");
    exit;
} catch (PDOException $e) {
    echo "<p style='color:red;'>Error al reiniciar la base de datos: " . htmlspecialchars($e->getMessage()) . "</p>";
}
?>
