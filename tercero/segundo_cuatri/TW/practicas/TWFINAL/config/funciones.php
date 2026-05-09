<?php
require_once 'config.php';

function iniciar_sesion() {
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
}

function obtener_pdo() {
    $host = 'localhost';
    $usuario = 'algarza042425';
    $clave = 'IzygpKa3IU8Ru1nF';
    $bd = 'algarza042425';
    $charset = 'utf8';
    $dsn = "mysql:host=$host;dbname=$bd;charset=$charset";
    $options = [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES   => FALSE,
    ];

    try {
        return new PDO($dsn, $usuario, $clave, $options);
    } catch (\PDOException $e) {
        throw new \PDOException($e->getMessage(), (int)$e->getCode());
    }
}

function esta_logueado() {
    return isset($_SESSION['rol']);
}

function es_admin() {
    return esta_logueado() && $_SESSION['rol'] === 'admin';
}

function mandar_a_login() {
    if (!esta_logueado()) {
        header("Location: index.php?page=login");
        exit;
    }
}

function mandar_a_inicio() {
    if (!es_admin()) {
        header("Location: index.php?page=inicio");
        exit;
    }
}

function registrar_evento($descripcion) {
    $pdo = obtener_pdo();
    $stmt = $pdo->prepare("INSERT INTO log (fecha_hora, descripcion) VALUES (NOW(), ?)");
    $stmt->execute([$descripcion]);
}

function redirigir_error($pagina, $tipo, $mensaje) {
    header("Location: ../index.php?page=$pagina&$tipo=$mensaje");
    exit;
}

function redirigir_mensaje($pagina, $tipo, $mensaje) {
    header("Location: ../index.php?page=$pagina&$tipo=$mensaje");
    exit;
}

?>