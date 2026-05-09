<?php
require_once('../config/funciones.php');
iniciar_sesion();
if (!es_admin()) {
    header("Location: ../index.php?page=inicio&error=permiso_denegado");
    exit;
}

$pdo = obtener_pdo();
$nombre_bd = $pdo->query("SELECT DATABASE()")->fetchColumn();
$tablas = $pdo->query("SHOW TABLES")->fetchAll(PDO::FETCH_COLUMN);

header('Content-Type: text/plain');
header('Content-Disposition: attachment; filename="backup_' . $nombre_bd . '_' . date('Ymd_His') . '.sql"');

echo "-- Copia de seguridad de la base de datos $nombre_bd\n";
echo "-- Fecha: " . date('Y-m-d H:i:s') . "\n\n";
echo "SET FOREIGN_KEY_CHECKS=0;\n\n";

foreach ($tablas as $tabla) {
    // DROP TABLE
    echo "DROP TABLE IF EXISTS `$tabla`;\n";

    // CREATE TABLE
    $create = $pdo->query("SHOW CREATE TABLE `$tabla`")->fetch(PDO::FETCH_ASSOC);
    echo $create['Create Table'] . ";\n\n";

    // DELETE (opcional, por si se restaura sobre una tabla existente)
    echo "DELETE FROM `$tabla`;\n";

    // INSERTS
    $rows = $pdo->query("SELECT * FROM `$tabla`")->fetchAll(PDO::FETCH_ASSOC);
    foreach ($rows as $row) {
        $values = array_map(function($v) use ($pdo) {
            if ($v === null) return "NULL";
            return $pdo->quote($v);
        }, array_values($row));
        echo "INSERT INTO `$tabla` VALUES (" . implode(", ", $values) . ");\n";
    }
    echo "\n";
}
echo "SET FOREIGN_KEY_CHECKS=1;\n";
exit;