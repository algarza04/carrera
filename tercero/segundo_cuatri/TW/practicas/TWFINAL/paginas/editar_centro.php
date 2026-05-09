<?php
/**
 * editar_centro.php
 * Página para que el administrador edite la configuración general del centro.
 * Requiere sesión activa como administrador.
 */

require_once('config/funciones.php');
iniciar_sesion();

if (!es_admin()) {
    header("Location: index.php?page=inicio&error=acceso_restringido");
}

// Obtener la configuración actual del centro
$resultado = $conexion->query("SELECT * FROM configuracion_centro WHERE id = 1");
if (!$resultado || $resultado->num_rows === 0) {
    header("Location: index.php?page=inicio&error=no_configuracion");
}
$config = $resultado->fetch_assoc();
?>

<h2>Editar configuración del centro</h2>

<form action="procesar/guardar_config_centro.php" method="post" enctype="multipart/form-data" novalidate>
    <label>Nombre del centro:
        <input type="text" name="nombre" value="<?= htmlspecialchars($config['nombre']) ?>" required>
    </label>

    <label>Descripción:
        <textarea name="descripcion" rows="4" cols="50"><?= htmlspecialchars($config['descripcion']) ?></textarea>
    </label>

    <label>Horario de apertura:
        <input type="time" name="hora_apertura" value="<?= $config['hora_apertura'] ?>">
    </label>

    <label>Horario de cierre:
        <input type="time" name="hora_cierre" value="<?= $config['hora_cierre'] ?>">
    </label>

    <label>Logo institucional:
        <input disabled type="file" name="logotipo">
    </label>

    <button type="submit" class="boton">Guardar cambios</button>
</form>