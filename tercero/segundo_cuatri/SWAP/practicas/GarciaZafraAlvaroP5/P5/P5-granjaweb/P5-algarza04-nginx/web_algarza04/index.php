<?php
header('Content-Type: application/json');

// Mostrar IP del servidor si se accede sin acción específica
if ($_SERVER['REQUEST_METHOD'] === 'GET' && empty($_GET['action'])) {
    $server_ip = $_SERVER['SERVER_ADDR'];
    echo '<h1>SWAP - "Álvaro García Zafra"</h1><br>';
    echo "Dirección IP del servidor: $server_ip \n";
    exit;
}

// Acción esperada
$action = $_GET['action'] ?? '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $action === 'login') {
    // Leer cuerpo JSON
    $input = json_decode(file_get_contents("php://input"), true);

    // Login simple
    $username = $input['username'] ?? '';
    $password = $input['password'] ?? '';

    if ($username === 'testuser' && $password === 'testpass') {
        $token = bin2hex(random_bytes(16)); // Token de prueba
        file_put_contents("token.txt", $token); // Guardar el token
        echo json_encode(["token" => $token]);
    } else {
        http_response_code(401);
        echo json_encode(["error" => "Credenciales inválidas"]);
    }
} else {
    http_response_code(400);
    echo json_encode(["error" => "Petición inválida"]);
}
?>
