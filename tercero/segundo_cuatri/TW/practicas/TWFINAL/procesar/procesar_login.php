<?php
/**
 * Fichero para procesar el inicio de sesión de usuarios
 * Verifica las credenciales y establece la sesión.
 * Redirige a la página de inicio o muestra un error.
 */
include_once '../config/funciones.php';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['inicio'])) {
    require_once '../config/config.php';
    session_start();

    $email = $_POST['email'];
    $clave = $_POST['clave'];

    $stmt = $conexion->prepare("SELECT id, clave, rol FROM usuarios WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows === 1) {
        $stmt->bind_result($id, $claveHash, $rol);
        $stmt->fetch();

        if (password_verify($clave, $claveHash)) {
            $_SESSION['id'] = $id;
            $_SESSION['email'] = $email;
            $_SESSION['rol'] = $rol;

            registrar_evento("Usuario identificado: " . $_SESSION['email']);
            header("Location: ../index.php?page=inicio");
            exit();
        }
    }

    $error = "El email o contraseña no es válido";
    registrar_evento("Intento de identificación erróneo con email: " . $_POST['email']);
    $params = http_build_query([
        'error' => json_encode($error),
        'datos' => json_encode(['email' => $email])
    ]);

    header("Location: ../index.php?page=login&$params");
    exit();
}

