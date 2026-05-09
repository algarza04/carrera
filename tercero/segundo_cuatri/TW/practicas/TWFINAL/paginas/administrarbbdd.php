<?php
/**
 * Página para administrar la base de datos
 * Permite reiniciar la base de datos, crear copias de seguridad y restaurar desde un archivo.
 */

require_once 'config/funciones.php';
iniciar_sesion();

if (!es_admin()) {
    header("Location: index.php?page=inicio&error=permiso_denegado");
    exit;
}
?>

<h2>Administrar Base de Datos</h2>

<form action="bbdd/reiniciar_BBDD.php" method="post" novalidate>
    <button type="submit" class="boton">
        Reiniciar Base de Datos
    </button>
</form>

<form action="bbdd/realizar_backup.php" method="post" novalidate>
    <button type="submit" class="boton">
        Crear Copia de Seguridad
    </button>
</form>

<form action="bbdd/importar_bbdd.php" method="post" enctype="multipart/form-data" novalidate>
    <button type="submit" class="boton">
        Restaurar Base de Datos
    </button>
    <input type="file" name="sql_file" id="backup_file" required style="margin-bottom: 10px;">
</form>

<a href="index.php?page=inicio" style="display: inline-block; margin-top: 20px; text-decoration: none; color: black; border: 1px solid black; padding: 10px;">
    Volver al Inicio
</a>