<?php
$datos = [
    'nombre' => '',
    'apellidos' => '',
    'dni' => '',
    'fecha_nacimiento' => '',
    'nacionalidad' => 'España',
    'sexo' => 'NA',
    'email' => '',
    'clave' => '',
    'clave_repetida' => '',
    'idioma' => 'Inglés',
    'aficiones' => [
        'música' => false,
        'leer' => true,
        'cine' => false,
        'deporte' => false
    ],
    'datos_almacenados' => 'TOTAL'
];
$errores = [];
$deshabilitado = false;
function letraCorrectaDNI($dni){
        $letra = substr($dni, -1);
        $numeros = substr($dni, 0, -1);  
    
        if (strlen($dni) != 9 || !is_numeric($numeros) || !preg_match('/^[A-Z]$/', $letra)) {
            return false;
        }
    
        $letrasValidas = "TRWAGMYFPDXBNJZSQVHLCKE";
        $letraCorrecta = $letrasValidas[$numeros % 23];
    
        // Comparar la letra proporcionada con la letra calculada
        return strtoupper($letra) === $letraCorrecta;
}

function mayorEdad($fecha_nacimiento){
    $fechaActual = new DateTime();
    $fechaNacimiento = new DateTime($fecha_nacimiento);
    $edad = $fechaActual->diff($fechaNacimiento)->y;
    return $edad >= 18;
}

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['envio'])){
    if (empty($_GET['nombre'])){
        $errores['nombre'] = 'El nombre es obligatorio';
    } else {
        $datos['nombre'] = $_GET['nombre'];
    }

    if (!empty($_GET['apellidos'])){
        $datos['apellidos'] = $_GET['apellidos'];
    } 

    if (empty($_GET['dni'])) {
        $errores['dni'] = 'El DNI es obligatorio';
    } elseif (!letraCorrectaDNI($_GET['dni'])) {
        $errores['dni'] = 'El DNI no es válido';
    } else {
        $datos['dni'] = $_GET['dni'];
    }

    if (empty($_GET['fecha_nacimiento'])) {
        $errores['fecha_nacimiento'] = 'Indique su edad';
    } elseif (!mayorEdad($_GET['fecha_nacimiento'])) {
        $errores['fecha_nacimiento'] = 'Debe ser mayor de edad';
    } else {
        $datos['fecha_nacimiento'] = $_GET['fecha_nacimiento'];
    }

    if (!empty($_GET['nacionalidad'])) {
        $datos['nacionalidad'] = $_GET['nacionalidad'];
    }

    if (empty($_GET['sexo']) || !in_array($_GET['sexo'], ['Masculino', 'Femenino', 'NA'])) {
        $errores['sexo'] = 'Seleccione un sexo válido';
    } else {
        $datos['sexo'] = $_GET['sexo'];
    }

    if (empty($_GET['email'])){
        $errores['email'] = 'El email es obligatorio';
    } elseif (!filter_var($_GET['email'], FILTER_VALIDATE_EMAIL)) {
        $errores['email'] = 'El email no es válido.';
    } else {
        $datos['email'] = $_GET['email'];
    }

    if (empty($_GET['clave'])){
        $errores['clave'] = 'Escriba su clave de acceso';
    } else {
        $datos['clave'] = $_GET['clave'];
    }

    if (($_GET['clave'] !== $_GET['clave_repetida']) || empty($_GET['clave_repetida'])) {
        $errores['clave_repetida'] = 'Ambas claves deben coincidir';
    } else {
        $datos['clave_repetida'] = $_GET['clave_repetida'];
    }

    if (empty($_GET['idioma'])) {
        $errores['idioma'] = 'Marque un idioma';
    } else {
        $datos['idioma'] = $_GET['idioma'];
    }

    $aficiones_validas = ['música', 'leer', 'cine', 'deporte'];
    foreach ($aficiones_validas as $aficion) {
        $datos['aficiones'][$aficion] = isset($_GET['aficiones']) && in_array($aficion, $_GET['aficiones']);
    }

    if (!empty($_GET['datos_almacenados']) && in_array($_GET['datos_almacenados'], ['TOTAL', 'PARCIAL', 'NINGUNO'])) {
        $datos['datos_almacenados'] = $_GET['datos_almacenados'];
    } 

    if (empty($errores)) {
        $deshabilitado = true;
    }
}

function Checked($value, $expected) {
    return ($value === $expected) ? 'checked' : '';
}

function CheckedCheckbox($value) {  //esta función es para los checkbox ya que con la anterior no funciona como esperamos
    return $value ? 'checked' : '';
}

function Selected($value, $expected) {
    return $value === $expected ? 'selected' : '';
}

function mostrarFormulario($datos, $errores, $deshabilitado = false) {
    $readonly = $deshabilitado ? 'readonly' : '';
    $disabled = $deshabilitado ? 'disabled' : '';
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ejercicio 7</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            border: black 1px solid;
            font-family: sans-serif;
            display: block;
        }

        header p{
            background-color: darkblue;
            color: white;
            text-align: center;
            font-size: 30px;
            padding: 10px 0;
            margin: 0 0 20px;
        }
        h1{
            background-color:  saddlebrown;
            color: white;
            margin: 0;
            padding: 5px;
        }

        h2{
            background-color:  peru;
            color: white;
            margin-top: -25px;
            margin-bottom: 20px;
            margin: -25px 0 20px 10px;
            padding: 5px;
            top: -50px;
            width: fit-content;
            border: 1px solid grey;
            font-size: 20px;
        }
        section{
            background-color: moccasin;
            border: 1px solid grey;
            margin: 25px 5px;
            padding: 5px 10px 5px 0px;
        }

        .datos_personales div {
            background-color: rgb(204, 171, 115);
            display: inline-block;
            margin: 5px;
            width: 100%;
            padding: 0;
        }

        div .alinear_datos {
            margin: 0;
            border-left: 3px solid sienna;
            width: 50%;
            float: left;
            display: inline;
            padding: 10px;
        }

        .datos_acceso label {
            padding-left: 10px;
        }

        p{
            margin-bottom: 0;
        }

        label{
            display: block;
            margin-left: 5px;
        }

        select{
            background-color: white;
            border: 1px solid grey;
        }

        .datos_adicionales1, .datos_adicionales2 {
            padding: 10px;
            width: calc(50% - 10px);
            display: inline-block;
            vertical-align: top;
            margin-top: 0;
        }

        .datos_adicionales1 h2, .datos_adicionales2 h2 {
            margin: -30px 0 0 0;
        }


        .botones_contenedor{
            text-align: center;
            border: 0;
            margin: 0px;
            padding: 0px;
            background-color: white;
        }
        .boton {
            margin: 25px 10px 5px;
            background-color: whitesmoke;
            border: 1px solid grey;
            color: dimgrey;
        }

        .error {
            color: red;
            font-style: italic;
            font-size: medium;
            margin-left: 30px;
        }

        section:not(.botones_contenedor):hover {
            border: 5px solid saddlebrown;
        }

        .datos_personales:hover::after {
            content: "Indique sus datos personales";
            color: saddlebrown;
            font-size: 14px;
            font-weight: bold;
            font-style: italic;
        }

        .datos_acceso:hover::after {
            content: "Indique cuales van a ser sus datos de acceso";
            color: saddlebrown;
            font-size: 14px;
            font-weight: bold;
            font-style: italic;
        }

        .datos_adicionales1:hover::after {
            content: "Este dato nos permitrá saber en que idioma desea comunicarse";
            color: saddlebrown;
            font-size: 14px;
            font-weight: bold;
            font-style: italic;
        }

        .datos_adicionales2:hover::after {
            content: "Este dato no es obligatorio pero nos facilitará el envio de la publicidad personalizada"; 
            color: saddlebrown;
            font-size: 14px;
            font-weight: bold;
            font-style: italic;
        }

        .boton:hover {
            background-color: saddlebrown;
            color: white;
            
        }
    </style>
</head>
<body>
    <header>
        <?php if($deshabilitado) echo '<p>Los datos se han recibido correctamente.</p>'?>
    </header>
    <h1>Registro de usuarios</h1>
    <form action="" method="GET" novalidate> 
        <section class="datos_personales">
            <h2>Datos personales</h2>
            <div>
                <div class="alinear_datos">
                    <label>Nombre 
                        <input type="text" name="nombre" size="20" value="<?= $datos['nombre'] ?>" required placeholder="El nombre es obligatorio" <?= $readonly ?>>
                    </label>  
                    <span class="error"><?= $errores['nombre'] ?? ''?></span>
                    <label>Apellidos
                        <input type="text" name="apellidos" size="30" value="<?= $datos['apellidos'] ?>" placeholder="Esto es opcional" <?= $readonly ?>>
                    </label>
                </div>
                <div class="alinear_datos">
                    <label>DNI
                        <input type="text" name="dni" value="<?= $datos['dni'] ?>" required size="9" <?= $readonly ?>>
                    </label>
                    <span class="error"><?= $errores['dni'] ?? '' ?></span>
                    <label>Fecha de nacimiento
                        <input type="date" name="fecha_nacimiento"  required value="<?= $datos['fecha_nacimiento'] ?>" <?= $readonly ?>>
                    </label>
                    <span class="error"><?= $errores['fecha_nacimiento'] ?? ''?></span>
                </div>
            </div>
        
            <div>
                <div class="alinear_datos">
                    <label>Nacionalidad
                        <input type="text" name="nacionalidad" value="<?= $datos['nacionalidad'] ?>" <?= $readonly ?>>
                    </label>
                    <label>Sexo
                        <select name="sexo" <?= $disabled?>>
                            <option value="Masculino" <?= Selected($datos['sexo'], 'Masculino') ?>>Masculino</option>
                            <option value="Femenino" <?= Selected($datos['sexo'], 'Femenino') ?>>Femenino</option>
                            <option value="NA" <?= Selected($datos['sexo'], 'NA') ?>>No deseo responder</option>
                        </select>
                    </label>
                    <span class="error"><?= $errores['sexo'] ?? ''?></span>
                </div>
                <div class="alinear_datos">
                    <label>Fotografía
                        <input type="file" name="foto" disabled>
                    </label>
                </div>
            </div>
        </section>
        <section class="datos_acceso">
            <h2>Datos de acceso</h2>
            <div>
                <label>E-mail
                    <input type="email" name="email" size="30" value="<?= $datos['email'] ?>" required <?= $readonly ?>>
                </label>
                <span class="error"><?= $errores['email'] ?? '' ?></span>
                <label>Clave
                    <input type="password" name="clave" size="15" value="<?= $datos['clave'] ?>" required placeholder="Escriba la clave" <?= $readonly ?>>
                </label>
                <span class="error"><?= $errores['clave'] ?? '' ?></span>
                <label>(repítala) 
                    <input type="password" name="clave_repetida" size="15" value="<?= $datos['clave_repetida'] ?>" required <?= $readonly ?>>
                </label>
                <span class="error"><?= $errores['clave_repetida'] ?? '' ?></span>
            </div>
        </section>
        <section class="datos_adicionales1">
            <h2>Datos adicionales 1</h2>
                <p>Idioma para comunicaciones: </p>
                <label><input type="radio" name="idioma" value="Español" <?= Checked($datos['idioma'], 'Español') ?> <?= $disabled ?>>Español</label>
                <label><input type="radio" name="idioma" value="Inglés" <?= Checked($datos['idioma'], 'Inglés') ?> <?= $disabled ?>>Inglés</label>
                <label><input type="radio" name="idioma" value="Francés" <?= Checked($datos['idioma'], 'Francés') ?> <?= $disabled ?>>Francés</label>
                <span class="error"><?= $errores['idioma'] ?? '' ?></span>
        </section
        ><section class="datos_adicionales2">
                <h2>Datos adicionales 2</h2>
                <p>Aficiones: </p>
                <label><input type="checkbox" name="aficiones[]" value="música"<?= CheckedCheckbox($datos['aficiones']['música']) ?> <?= $disabled ?>>La música</label>
                <label><input type="checkbox" name="aficiones[]" value="leer"  <?= CheckedCheckbox($datos['aficiones']['leer']) ?> <?= $disabled ?>>Leer libros</label>
                <label><input type="checkbox" name="aficiones[]" value="cine" <?= CheckedCheckbox($datos['aficiones']['cine']) ?> <?= $disabled ?>>El cine</label>
                <label><input type="checkbox" name="aficiones[]" value="deporte" <?= CheckedCheckbox($datos['aficiones']['deporte']) ?> <?= $disabled ?>>El deporte</label>
        </section>

        <label>Tratamiento de datos
            <select name="datos_almacenados" <?= $disabled ?>>
                <option value="TOTAL" <?= Selected($datos['datos_almacenados'], 'TOTAL') ?>>Acepta el almacenamiento de mis datos y el envío a terceros</option>
                <option value="PARCIAL" <?= Selected($datos['datos_almacenados'], 'PARCIAL') ?>>Acepta el almacenamiento de mis datos pero no el envío a terceros</option>
                <option value="NINGUNO" <?= Selected($datos['datos_almacenados'], 'NINGUNO') ?>>No acepta el almacenamiento ni el envío de datos a terceros</option>
            </select>
        </label>

        <div class="botones_contenedor">
            <?php if ($deshabilitado): ?>
                <input class="boton" type="submit" value="Confirmar datos"> <!-- Esto cargara "un nuevo formulario"-->
            <?php else: ?>
                <input class="boton" type="submit" value="Enviar datos" name="envio">
                <input class="boton" type="reset" value="Borrar formulario" name="borrar">  
            <?php endif; ?>
        </div>
    </form>
</body>
</html>

<?php        
}

mostrarFormulario($datos, $errores, $deshabilitado);
?>
