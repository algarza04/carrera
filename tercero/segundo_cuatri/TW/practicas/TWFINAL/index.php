<?php 
require_once 'config/funciones.php';
iniciar_sesion();

$pdo = obtener_pdo();

// Obtener la configuración del centro
$stmt = $pdo->query("SELECT nombre, logotipo FROM configuracion_centro LIMIT 1");
$configuracion = $stmt->fetch(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title><?= htmlspecialchars($configuracion['nombre']) ?></title>
    <link rel="stylesheet" href="pfinal.css">
</head>
<body>
    <header>
        <div>
            <img src=<?= htmlspecialchars($configuracion['logotipo']) ?> alt="Logotipo centro" class="logougr">
            <h1><?= htmlspecialchars($configuracion['nombre']) ?></h1>
        </div>
        <nav>
            <ul>
                <li><a href="index.php?page=inicio">Inicio</a></li>
                <li><a href="index.php?page=listar_salas">Salas</a></li>
                <li><a href="index.php?page=buscar_reservas">Reservas</a></li>
                <?php if (esta_logueado()): ?>
                <li><a href="index.php?page=reservas">Reservar</a></li>
                <?php endif; ?>
                <?php if (es_admin()): ?>
                <li><a href="index.php?page=editar_sala">Crear sala</a></li>
                <li><a href="index.php?page=editar_centro">Editar centro</a></li>
                <li><a href="index.php?page=registro">Crear usuario</a></li>
                <li><a href="index.php?page=listar_usuarios">Usuarios registrados</a></li>
                <li><a href="index.php?page=listar_logs">Logs</a></li>
                <li><a href="index.php?page=BBDD">Administrar BBDD</a></li>
                <?php endif; ?>
            </ul>
        </nav>
    </header>

    <main>
        <section>

        <?php
            $pagina = $_GET['page'] ?? 'inicio';

            switch ($pagina) {
                case 'login':
                    if (esta_logueado()) {
                        header("Location: index.php?page=inicio&error=ya_logueado");
                        exit;
                    }
                    include 'paginas/login.php';
                    break;

                case 'logout':
                    if (!esta_logueado()) {
                        header("Location: index.php?page=inicio&error=no_logueado");
                        exit;
                    }
                    include 'paginas/logout.php';
                    break;

                case 'registro':
                    if (esta_logueado() && !es_admin()) {
                        header("Location: index.php?page=inicio&error=ya_logueado");
                        exit;
                    }
                    include 'paginas/registro.php';
                    break;

                case 'perfil':
                    if (!esta_logueado()) {
                        header("Location: index.php?page=login&error=no_logueado");
                        exit;
                    }
                    include 'paginas/perfil.php';
                    break;

                case 'reservas':
                    if (!esta_logueado()) {
                        header("Location: index.php?page=login&error=no_logueado");
                        exit;
                    }
                    include 'paginas/reservas.php';
                    break;

                case 'inicio':
                    include 'paginas/inicio.php';
                    break;

                case 'listar_salas':
                    if (!esta_logueado()) {
                        header("Location: index.php?page=login&error=no_logueado");
                        exit;
                    }
                    include 'paginas/listar_salas.php';
                    break;

                case 'editar_sala':
                    if (!es_admin()) {
                        header("Location: index.php?page=inicio&error=permiso_denegado");
                        exit;
                    }
                    include 'paginas/editar_sala.php';
                    break;
                
                case 'sala':
                    include 'paginas/sala.php';
                    break;

                case 'listar_usuarios':
                    if (!es_admin()) {
                        header("Location: index.php?page=inicio&error=permiso_denegado");
                        exit;
                    }
                    include 'paginas/listar_usuarios.php';
                    break;

                case 'editar_perfil':
                    if (!esta_logueado()) {
                        header("Location: index.php?page=login");
                        exit;
                    }
                    include 'paginas/editar_perfil.php';
                    break;
                
                case 'editar_centro':
                    if (!es_admin()) {
                        header("Location: index.php?page=inicio&error=permiso_denegado");
                        exit;
                    }
                    include 'paginas/editar_centro.php';
                    break;

                case 'listar_logs':
                    if (!es_admin()) {
                        header("Location: index.php?page=inicio&error=permiso_denegado");
                        exit;
                    }
                    include 'paginas/listar_logs.php';
                    break;

                case 'BBDD':
                    if (!es_admin()) {
                        header("Location: index.php?page=inicio&error=permiso_denegado");
                        exit;
                    }
                    include 'paginas/administrarbbdd.php';
                    break;

                case 'buscar_reservas':
                    include 'paginas/buscar_reservas.php';
                    break;

                case 'listar_reservas':
                    include 'paginas/listar_reservas_vista.php';
                    break;

                default:
                    include 'paginas/inicio.php';
                    break;
            }
        ?>
        </section>
        <aside>
            <nav>
                <?php if (!esta_logueado()): ?>
                <p>Actualmente no estás logueado, inicia sesión para obtener más privilegios.</p>
                <p><a href="index.php?page=registro">Registrarse</a></p>
                <p><a href="index.php?page=login">Login</a></p>
                <?php else: ?>
                    <?php if (es_admin()): ?>
                    <p style="padding:10px;">¡Bienvenido, administrador <?= htmlspecialchars($_SESSION['email']) ?>!</p>
                    <?php else: ?>
                    <p style="padding:10px;">¡Bienvenido, cliente <?= htmlspecialchars($_SESSION['email']) ?>!</p>
                    <?php endif; ?>
                    <?php if (!empty($_SESSION['foto'])): ?>
                        <img <?= htmlspecialchars($_SESSION['foto']) ?> alt="Foto de perfil" style="width:100px; height:auto; border-radius:50%;">
                    <?php else: ?>
                        <img src="imagenes/imagen_perfil.png" alt="Foto por defecto" style="width:100px; height:auto; border-radius:50%;">
                    <?php endif; ?>
                    <p><a href="index.php?page=perfil">Perfil</a></p>
                    <p><a href="index.php?page=logout">Logout</a></p>
                <?php endif; ?>
                <?php
                $pdo = obtener_pdo();
                $total_salas = $pdo->query("SELECT COUNT(*) FROM salas")->fetchColumn();
                $total_asientos = $pdo->query("SELECT SUM(puestos) FROM salas")->fetchColumn();
                $hoy = date('Y-m-d');
                $stmt = $pdo->prepare("SELECT COUNT(DISTINCT sala_id) FROM reservas WHERE fecha = ?");
                $stmt->execute([$hoy]);
                $salas_reservadas = $stmt->fetchColumn();
                ?>
                <div style="padding:10px;">
                    <strong>Aulas del edificio:</strong> <?= $total_salas ?><br>
                    <strong>Asientos totales:</strong> <?= $total_asientos ?><br>
                    <strong>Aulas reservadas hoy:</strong> <?= $salas_reservadas ?>
                </div>
            </nav>
        </aside>
    </main>

   

    <footer>
        <p>&copy; 2025 ETSIIT - Universidad de Granada</p>
        <p>Álvaro García Zafra y Fernando Castilla Ropero</p>
        <p><a href="docProyectoTW.pdf">Documentación de la práctica</a></p>
        <p><a href="backup_algarza042425_20250603_200841.sql">Restauración de la BBDD</a></p>
    </footer>
</body>
</html>
