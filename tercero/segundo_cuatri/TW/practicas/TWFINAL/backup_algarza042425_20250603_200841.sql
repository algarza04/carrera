-- Copia de seguridad de la base de datos algarza042425
-- Fecha: 2025-06-03 21:04:43

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `comentarios`;
CREATE TABLE `comentarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sala_id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `texto` text CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `sala_id` (`sala_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `comentarios_ibfk_1` FOREIGN KEY (`sala_id`) REFERENCES `salas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `comentarios_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `comentarios`;
INSERT INTO `comentarios` VALUES ('1', '1', '1', 'Este aula es muy buena para los examenes.', '2025-06-03 20:32:28');
INSERT INTO `comentarios` VALUES ('2', '2', '1', 'Aire estropeado', '2025-06-03 20:33:14');

DROP TABLE IF EXISTS `configuracion_centro`;
CREATE TABLE `configuracion_centro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `logotipo` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `descripcion` text CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `hora_apertura` time NOT NULL,
  `hora_cierre` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `configuracion_centro`;
INSERT INTO `configuracion_centro` VALUES ('1', 'ETSIIT', 'imagenes/centro/log_centro.png', 'Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación (ETSIIT) es un centro docente de la Universidad de Granada situado en el campus Aynadamar,junto a la Facultad de Bellas Artes. docente.\r\nLos grados en Ingeniería Informática e Ingeniería en Tecnologías de Telecomunicaciónde la UGR han obtenido los sellos internacionales de calidad EURO-INF y EURO-ACE respectivamente concedidos por la European Quality Assurance Network for Informatics Education (EQANIE) en el caso de EUROINF y por la European Network for the Accreditation of Engineering Education (ENAEE) en el caso de EUROACE', '09:00:00', '19:00:00');

DROP TABLE IF EXISTS `fotos`;
CREATE TABLE `fotos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `referencia_id` int NOT NULL,
  `tipo` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL DEFAULT 'sala',
  `contenido` longblob NOT NULL,
  `mime_type` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `referencia_id` (`referencia_id`),
  CONSTRAINT `fotos_ibfk_1` FOREIGN KEY (`referencia_id`) REFERENCES `salas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `fotos`;

DROP TABLE IF EXISTS `log`;
CREATE TABLE `log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_hora` datetime NOT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `log`;
INSERT INTO `log` VALUES ('1', '2025-06-03 20:19:12', 'Base de datos reiniciada por el administrador admin@void.ugr.es');
INSERT INTO `log` VALUES ('2', '2025-06-03 20:19:36', 'Usuario identificado: admin@void.ugr.es');
INSERT INTO `log` VALUES ('3', '2025-06-03 20:23:02', 'Nuevo usuario registrado: javier@void.ugr.es');
INSERT INTO `log` VALUES ('4', '2025-06-03 20:24:22', 'Nuevo usuario registrado: pedro@void.ugr.es');
INSERT INTO `log` VALUES ('5', '2025-06-03 20:24:24', 'El usuario admin@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('6', '2025-06-03 20:24:36', 'Usuario identificado: javier@void.ugr.es');
INSERT INTO `log` VALUES ('7', '2025-06-03 20:24:38', 'El usuario javier@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('8', '2025-06-03 20:24:46', 'Usuario identificado: pedro@void.ugr.es');
INSERT INTO `log` VALUES ('9', '2025-06-03 20:24:49', 'El usuario pedro@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('10', '2025-06-03 20:25:26', 'Nuevo usuario registrado: anita@void.ugr.es');
INSERT INTO `log` VALUES ('11', '2025-06-03 20:25:35', 'Usuario identificado: anita@void.ugr.es');
INSERT INTO `log` VALUES ('12', '2025-06-03 20:25:36', 'El usuario anita@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('13', '2025-06-03 20:29:28', 'Nuevo usuario registrado: maria@void.ugr.es');
INSERT INTO `log` VALUES ('14', '2025-06-03 20:29:49', 'Usuario identificado: maria@void.ugr.es');
INSERT INTO `log` VALUES ('15', '2025-06-03 20:31:03', 'El usuario maria@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('16', '2025-06-03 20:31:09', 'Usuario identificado: admin@void.ugr.es');
INSERT INTO `log` VALUES ('17', '2025-06-03 20:39:03', 'El usuario admin@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('18', '2025-06-03 20:39:16', 'Usuario identificado: javier@void.ugr.es');
INSERT INTO `log` VALUES ('19', '2025-06-03 20:45:04', 'El usuario javier@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('20', '2025-06-03 20:45:35', 'Usuario identificado: admin@void.ugr.es');
INSERT INTO `log` VALUES ('21', '2025-06-03 20:46:41', 'El usuario admin@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('22', '2025-06-03 20:48:16', 'Usuario identificado: pedro@void.ugr.es');
INSERT INTO `log` VALUES ('23', '2025-06-03 20:49:53', 'El usuario pedro@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('24', '2025-06-03 20:50:00', 'Usuario identificado: admin@void.ugr.es');
INSERT INTO `log` VALUES ('25', '2025-06-03 20:51:54', 'El usuario admin@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('26', '2025-06-03 20:52:46', 'Usuario identificado: anita@void.ugr.es');
INSERT INTO `log` VALUES ('27', '2025-06-03 20:55:25', 'El usuario anita@void.ugr.es cerró sesión: ');
INSERT INTO `log` VALUES ('28', '2025-06-03 20:55:33', 'Usuario identificado: admin@void.ugr.es');
INSERT INTO `log` VALUES ('29', '2025-06-03 20:56:34', 'Nuevo usuario registrado: a@a.c');
INSERT INTO `log` VALUES ('30', '2025-06-03 21:00:05', 'Nuevo usuario registrado: q@a.d');
INSERT INTO `log` VALUES ('31', '2025-06-03 21:01:37', 'Nuevo usuario registrado: q@a.d');

DROP TABLE IF EXISTS `reservas`;
CREATE TABLE `reservas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `sala_id` int NOT NULL,
  `motivo` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `sala_id` (`sala_id`),
  CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`sala_id`) REFERENCES `salas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `reservas`;
INSERT INTO `reservas` VALUES ('2', '2', '6', 'Conferencia TW', '2025-06-03', '11:00:00', '12:00:00');
INSERT INTO `reservas` VALUES ('3', '2', '7', 'Exposición IA', '2025-06-03', '13:00:00', '14:00:00');
INSERT INTO `reservas` VALUES ('5', '2', '2', 'examenTW', '2025-06-03', '16:00:00', '17:00:00');
INSERT INTO `reservas` VALUES ('6', '1', '7', 'Reformas', '2025-06-03', '11:00:00', '12:00:00');
INSERT INTO `reservas` VALUES ('7', '1', '7', 'Reformas', '2025-06-03', '10:00:00', '11:00:00');
INSERT INTO `reservas` VALUES ('8', '3', '3', 'examen IA', '2025-06-03', '16:00:00', '17:00:00');
INSERT INTO `reservas` VALUES ('9', '3', '5', 'Examen MP', '2025-07-01', '11:00:00', '12:00:00');
INSERT INTO `reservas` VALUES ('10', '3', '3', 'Defensa', '2025-06-01', '09:00:00', '10:00:00');
INSERT INTO `reservas` VALUES ('11', '1', '4', 'Pruebas', '2025-06-19', '10:00:00', '11:00:00');
INSERT INTO `reservas` VALUES ('12', '1', '4', 'Pruebas', '2025-06-19', '09:00:00', '10:00:00');
INSERT INTO `reservas` VALUES ('13', '4', '2', 'Club de lectura', '2025-06-06', '15:00:00', '16:00:00');
INSERT INTO `reservas` VALUES ('14', '4', '2', 'Club de lectura', '2025-06-13', '15:00:00', '16:00:00');
INSERT INTO `reservas` VALUES ('15', '4', '5', 'Ensayo teatro', '2025-06-18', '09:00:00', '10:00:00');
INSERT INTO `reservas` VALUES ('16', '4', '2', 'Club de lectura', '2025-06-27', '15:00:00', '16:00:00');
INSERT INTO `reservas` VALUES ('17', '1', '6', 'Graduación', '2025-06-02', '10:00:00', '11:00:00');

DROP TABLE IF EXISTS `salas`;
CREATE TABLE `salas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `ubicacion` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `puestos` int NOT NULL,
  `descripcion` text CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci,
  `reservable` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `salas`;
INSERT INTO `salas` VALUES ('1', 'Aula 0.1', 'planta baja', '60', 'Aula para impartir docencia.', '1');
INSERT INTO `salas` VALUES ('2', 'Aula 0.2', 'planta baja', '70', 'Aula ideal para examenes.', '1');
INSERT INTO `salas` VALUES ('3', 'aula0.3', 'planta baja', '80', 'Aula ideal para examenes, no incluye proyector.', '1');
INSERT INTO `salas` VALUES ('4', 'Lab electrónica ', 'primera planta', '18', 'Aula diseñada para aprender de circuitos.', '1');
INSERT INTO `salas` VALUES ('5', 'Polivalente', 'Tercera planta', '30', 'Aula para cualquier uso.', '1');
INSERT INTO `salas` VALUES ('6', 'Salón de actos ', 'Planta -1', '150', 'Aula ideal para charlas', '0');
INSERT INTO `salas` VALUES ('7', 'Salón de grados  ', 'Planta auxiliar', '80', 'Zona para eventos.', '0');
INSERT INTO `salas` VALUES ('8', 'Lab 2.1', 'Planta 2', '38', 'Aula para impartir clases de prácticas.', '1');

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `apellidos` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `dni` varchar(9) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `clave` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci NOT NULL,
  `rol` enum('admin','cliente') CHARACTER SET utf8mb3 COLLATE utf8mb3_spanish_ci DEFAULT 'cliente',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dni` (`dni`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

DELETE FROM `usuarios`;
INSERT INTO `usuarios` VALUES ('1', 'admin', 'admin', '12345678Z', 'admin@void.ugr.es', '$2y$10$CXey8K7/zFBBG6s4zQ6aOemcLF5NOr107lfk5QP.6AGkixraPPGee', 'admin', '2025-06-03 20:19:12');
INSERT INTO `usuarios` VALUES ('2', 'Javier', 'Javier', '87654321X', 'javier@void.ugr.es', '$2y$10$Seij4dv77ZJKIPPAsuIUOOathv.B5jiP040.GIe3KR.w/vGs6zXWS', 'admin', '2025-06-03 20:23:02');
INSERT INTO `usuarios` VALUES ('3', 'Pedro', 'Pedro', '11111111H', 'pedro@void.ugr.es', '$2y$10$GIvVmF6pFXtXDAxaY1XGzO9lq9ZtnG6hJ7itLQTbU8X3MH95e4ksm', 'cliente', '2025-06-03 20:24:21');
INSERT INTO `usuarios` VALUES ('4', 'Anita', 'Anita', '22222222J', 'anita@void.ugr.es', '$2y$10$zAUbcYT1hggWV1kBretsLuPylVi1xZpSVz84LJ5Vta.CY16RZUSm2', 'cliente', '2025-06-03 20:25:26');
INSERT INTO `usuarios` VALUES ('5', 'maria', 'maria', '77689984D', 'maria@void.ugr.es', '$2y$10$q.CCohdpT3vacJmLlYmBhOyy94ginvLv0V7y84o.x466S9pQmdlea', 'cliente', '2025-06-03 20:29:28');

SET FOREIGN_KEY_CHECKS=1;
