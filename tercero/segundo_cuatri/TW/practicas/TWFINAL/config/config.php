<?php
$host = 'localhost';
$usuario = 'algarza042425';
$clave = 'IzygpKa3IU8Ru1nF';
$bd = 'algarza042425';

$conexion = new mysqli($host, $usuario, $clave, $bd);
if ($conexion->connect_error) {
    die('Error de conexión: ' . $conexion->connect_error);
}
$conexion->set_charset('utf8');
?>