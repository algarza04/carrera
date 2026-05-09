<?php
/**
 * Fichero para procesar el registro de nuevos usuarios
 * Valida los datos, comprueba si el DNI y email ya existen,
 * y redirige a la confirmación o inserta en la base de datos.
 * Permite asignar un rol (cliente o administrador) si el usuario es admin.
 * Redirige a la página de inicio de sesión tras el registro exitoso.
 */
require_once '../config/funciones.php';

function letraCorrectaDNI($dni) {
    $letras = 'TRWAGMYFPDXBNJZSQVHLCKE';
    if (preg_match('/^[0-9]{8}[A-Z]$/', $dni)) {
        $numero = substr($dni, 0, 8);
        $letra = substr($dni, -1);
        return $letra === $letras[intval($numero) % 23];
    }
    return false;
}

$errores = [];
$datos = [
    'nombre' => '',
    'apellidos' => '',
    'dni' => '',
    'email' => '',
    'clave' => '',
    'clave_repetida' => '',
    'rol' => ''
];

// PRIMER ENVÍO: Validar y pedir confirmación
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['envio'])) {
    $datos['nombre'] = $_POST['nombre'] ?? '';
    $datos['apellidos'] = $_POST['apellidos'] ?? '';
    $datos['dni'] = $_POST['dni'] ?? '';
    $datos['email'] = $_POST['email'] ?? '';
    $datos['clave'] = $_POST['clave'] ?? '';
    $datos['clave_repetida'] = $_POST['clave_repetida'] ?? '';

    if (empty($datos['nombre'])) {
        $errores['nombre'] = 'El nombre es obligatorio';
    }
    if (empty($datos['apellidos'])) {
        $errores['apellidos'] = 'Los apellidos son obligatorios';
    }
    if (empty($datos['dni'])) {
        $errores['dni'] = 'El DNI es obligatorio';
    } elseif (!letraCorrectaDNI($datos['dni'])) {
        $errores['dni'] = 'El DNI no es válido';
    }
    if (empty($datos['email'])) {
        $errores['email'] = 'El email es obligatorio';
    } elseif (!filter_var($datos['email'], FILTER_VALIDATE_EMAIL)) {
        $errores['email'] = 'El email no es válido';
    }
    if (empty($datos['clave'])) {
        $errores['clave'] = 'La clave es obligatoria';
    } elseif (strlen($datos['clave']) < 4) {
        $errores['clave'] = 'La clave debe tener al menos 4 caracteres';
    }
    if ($datos['clave'] !== $datos['clave_repetida'] || empty($datos['clave_repetida'])) {
        $errores['clave_repetida'] = "Las contraseñas no coinciden";
    }

    if (empty($errores)) {
        iniciar_sesion();
        $pdo = obtener_pdo();

        // Comprobar si el DNI ya existe
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM usuarios WHERE dni = ?");
        $stmt->execute([$datos['dni']]);
        if ($stmt->fetchColumn() > 0) {
            $errores['dni'] = "El DNI proporcionado ya está asociado a una cuenta.";
        }

        // Comprobar si el email ya existe
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM usuarios WHERE email = ?");
        $stmt->execute([$datos['email']]);
        if ($stmt->fetchColumn() > 0) {
            $errores['email'] = "El email proporcionado ya está asociado a una cuenta.";
        }
    }

    // SOLO UNA ASIGNACIÓN DE ROL
    $es_admin = es_admin();
    $datos['rol'] = ($es_admin && isset($_POST['rol'])) ? $_POST['rol'] : 'cliente';

    if (empty($errores)) {
        // Redirigir a confirmación (clave sin hashear)
        $params = http_build_query([
            'datos' => json_encode($datos),
            'confirmar' => 1
        ]);
        header("Location: ../index.php?page=registro&$params");
        exit;
    } else {
        // Redirigir con errores
        $params = http_build_query([
            'datos' => json_encode($datos),
            'errores' => json_encode($errores)
        ]);
        header("Location: ../index.php?page=registro&$params");
        exit;
    }
}

// SEGUNDO ENVÍO: Insertar en la base de datos
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['envio_final'])) {
    $datos['nombre'] = $_POST['nombre'] ?? '';
    $datos['apellidos'] = $_POST['apellidos'] ?? '';
    $datos['dni'] = $_POST['dni'] ?? '';
    $datos['email'] = $_POST['email'] ?? '';
    $clave_plana = $_POST['clave'] ?? '';
    $datos['clave'] = password_hash($clave_plana, PASSWORD_DEFAULT);
    $datos['rol'] = $_POST['rol'] ?? 'cliente';

    iniciar_sesion();
    $pdo = obtener_pdo();

    $stmt = $pdo->prepare("INSERT INTO usuarios (nombre, apellidos, dni, email, clave, rol) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->execute([
        $datos['nombre'],
        $datos['apellidos'],
        $datos['dni'],
        $datos['email'],
        $datos['clave'],
        $datos['rol']
    ]);

    registrar_evento("Nuevo usuario registrado: " . $datos['email']);
    if (es_admin()) {
        header("Location: ../index.php?page=listar_usuarios&mensaje=usuario_creado");
        exit;
    } else {
        header("Location: ../index.php?page=login&mensaje=registro_ok");
        exit;
    }
}