
<?php
/**
 * Editar o crear una sala
 */
require_once 'config/funciones.php';

iniciar_sesion();
$pdo = obtener_pdo();

if (!isset($_SESSION['rol']) || $_SESSION['rol'] !== 'admin') {
    header("Location: index.php");
    exit;
}

$id = $_GET['id'] ?? null;
$sala = [
    'nombre' => '',
    'ubicacion' => '',
    'puestos' => '',
    'descripcion' => '',
    'reservable' => 1
];

if ($id) {
    $stmt = $pdo->prepare("SELECT * FROM salas WHERE id = ?");
    $stmt->execute([$id]);
    $sala = $stmt->fetch(PDO::FETCH_ASSOC);
    if (!$sala) {
        echo "Sala no encontrada";
        exit;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'];
    $ubicacion = $_POST['ubicacion'];
    $puestos = intval($_POST['puestos']);
    $descripcion = $_POST['descripcion'];
    $reservable = isset($_POST['reservable']) ? 1 : 0;

    if ($id) {
        $stmt = $pdo->prepare("UPDATE salas SET nombre=?, ubicacion=?, puestos=?, descripcion=?, reservable=? WHERE id=?");
        $stmt->execute([$nombre, $ubicacion, $puestos, $descripcion, $reservable, $id]);
    } else {
        $stmt = $pdo->prepare("INSERT INTO salas (nombre, ubicacion, puestos, descripcion, reservable) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$nombre, $ubicacion, $puestos, $descripcion, $reservable]);
        $id = $pdo->lastInsertId();
    }

    header("Location: index.php?page=sala&id=" . $id);
    exit;
}
?>

<form method="post" novalidate>
    <label>Nombre: <input type="text" name="nombre" value="<?= htmlspecialchars($sala['nombre']) ?>" required></label>
    <label>Ubicación: <input type="text" name="ubicacion" value="<?= htmlspecialchars($sala['ubicacion']) ?>" required></label>
    <label>Puestos: <input type="number" name="puestos" value="<?= htmlspecialchars($sala['puestos']) ?>" min="1" required></label>
    <label>Descripción:
        <textarea name="descripcion"><?= htmlspecialchars($sala['descripcion']) ?></textarea>
    </label>
    <label>Reservable: <input type="checkbox" name="reservable" <?= $sala['reservable'] ? 'checked' : '' ?>></label>

    <button type="submit" class="boton">Guardar</button>
</form>
