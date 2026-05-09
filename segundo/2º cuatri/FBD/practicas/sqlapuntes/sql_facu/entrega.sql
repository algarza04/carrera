----------------------------------------------------------------------------------------------
-----------------------------EJERCICIOS APARTADO 1--------------------------------------------
----------------------------------------------------------------------------------------------

--Ejercicio 1.1 Ver la descripción de la tabla prueba1.
DESCRIBE prueba1

--Ejercicio 1.4 Borrar la tabla prueba1 y comprobar las tablas que quedan.
DROP TABLE prueba1

--Ejercicio 1.5 Modifica el esquema de la tabla plantilla añadiendo un nuevo atributo llamado fechabaja de tipo date.
ALTER TABLE plantilla ADD (fechabaja DATE)

--Ejercicio 1.6 Comprobar que se ha cambiado correctamente el esquema de la tabla Ventas.
DESCRIBE ventas






----------------------------------------------------------------------------------------------
-----------------------------EJERCICIOS APARTADO 2--------------------------------------------
----------------------------------------------------------------------------------------------

--Ejercicio 2.1 Ejecuta la sentencia SELECT para mostrar el contenido de las tablas PRUEBA2 y PLANTILLA.
SELECT * FROM prueba2;
SELECT * FROM plantilla;

--Ejercicio 2.2 Ejecuta la sentencia UPDATE sobre la tabla plantilla y cambia el nombre del trabajador con dni ’12345678’ a ’Luis’.
UPDATE plantilla
SET nombre = 'Luis'
WHERE dni = '12345678'


--LOS DEMAS EJERCICIOS VIENEN RESUELTOS Y LA LIGA DE BALONCESTO ESTA CREADA







----------------------------------------------------------------------------------------------
-----------------------------EJERCICIOS APARTADO 3--------------------------------------------
----------------------------------------------------------------------------------------------
--Ejercicio 3.3 Muestra las piezas de Madrid que son grises o rojas.
SELECT pieza.nompie from pieza where (color = 'rojo' or color = 'gris') and ciudad = 'Madrid'; 

--Ejercicio 3.4 Encontrar todos los suministros cuya cantidad está entre 200 y 300, ambos inclusive.
SELECT codpro FROM ventas WHERE cantidad >= 200 and cantidad <= 300

--Ejercicio 3.5 Mostrar las piezas que contengan la palabra tornillo con la t en mayúscula o en minúscula.
SELECT nompie FROM pieza WHERE nompie LIKE '%ornillo'

--Ejercicio 7 a 11 son de realizar comprobaciones

--Ejercicio 3.15 Mostrar las piezas vendidas por los proveedores de Madrid.
SELECT nompie,nompro FROM pieza NATURAL JOIN (SELECT * FROM proveedor WHERE ciudad = 'Madrid')
o
SELECT nompie,nompro FROM pieza p JOIN (SELECT * FROM proveedor WHERE ciudad = 'Madrid') v ON
(p.ciudad = v.ciudad)

--Ejercicio 3.16 Encuentra la ciudad y los códigos de las piezas suministradas a cualquier proyecto por un proveedor que está en la misma ciudad donde está el proyecto.
SELECT p.ciudad,v.codpie FROM proyecto p
JOIN ventas v ON v.codpj = p.codpj
JOIN proveedor pr ON  v.codpro = pr.codpro
WHERE pr.ciudad = p.ciudad

--Ejercicio 3.17 Comprobar la salida de la consulta anterior sin la cláusula ORDER BY.
Como se menciona anteriormente la salida de order by por defecto es creciente, en este caso de A a Z

--Ejercicio 3.18 Listar las ventas ordenadas por cantidad, si algunas ventas coinciden en la cantidad se ordenan en función de la fecha de manera descendente.
SELECT * FROM ventas
ORDER BY cantidad ASC, fecha DESC

--Ejercicio 3.19 Mostrar las piezas vendidas por los proveedores de Madrid. (Fragmentando la consulta con ayuda del operador IN.) Compara la solución con la del ejercicio 3.15.
SELECT codpie FROM ventas 
WHERE codpro IN (SELECT codpro FROM proveedor WHERE ciudad = 'Madrid')

--Ejercicio 3.20 Encuentra los proyectos que están en una ciudad donde se fabrica alguna pieza.
SELECT codpj FROM proyecto p JOIN (SELECT * FROM PIEZA) pi ON (p.ciudad = pi.ciudad)
ORDER BY codpj ASC

--Ejercicio 3.22 Muestra el código de las piezas cuyo peso es mayor que el peso de cualquier ’tornillo’.
SELECT codpie FROM pieza
WHERE peso > ALL (SELECT peso FROM pieza WHERE nompie LIKE 'Tornillo%');

--Ejercicio 3.23 Encuentra las piezas con peso máximo. Compara esta solución con la obtenida en el ejercicio 3.14
SELECT codpie FROM pieza
WHERE EXISTS (SELECT peso FROM pieza WHERE peso = 100);

--Ejercicio 3.26 Encontrar el número de envíos con más de 1000 unidades.
SELECT COUNT(cantidad) AS envios FROM ventas 
WHERE cantidad > 1000


--Ejercicio 3.27 Mostrar el máximo peso.
SELECT MAX(peso) FROM pieza

--Ejercicio 3.28 Mostrar el código de la pieza de máximo peso. Compara esta solución con las correspondientes de los ejercicios 3.14 y 3.23.
SELECT codpie FROM pieza
WHERE peso = (SELECT MAX(peso) FROM pieza)

--Ejercicio 3.29 Comprueba si la siguiente sentencia resuelve el ejercicio anterior.
 No

--Ejercicio 3.30 Muestra los códigos de proveedores que han hecho más de 3 envíos diferentes.
SELECT codpro FROM ventas
GROUP BY codpro
HAVING COUNT(codpro) > 3

--Ejercicio 3.31 Mostrar la media de las cantidades vendidas por cada código de pieza junto con su nombre.
SELECT p.nompie, ROUND(AVG(v.cantidad), 3) AS promedio FROM pieza p, ventas v
WHERE v.codpie = p.codpie
GROUP BY p.nompie

--Ejercicio 3.32 Encontrar la cantidad media de ventas de la pieza ’P1’ realizadas por cada proveedor.
SELECT codpro, AVG(cantidad) AS media FROM ventas
where codpie = 'P1'
GROUP BY codpro

--Ejercicio 3.33 Encontrar la cantidad total de cada pieza enviada a cada proyecto.
SELECT codpie,codpj, SUM(cantidad) AS total FROM ventas
GROUP BY (codpie,codpj)

--Ejercicio 3.34 Comprueba si es correcta la solución anterior.
 SI

--Ejercicio 3.35 Mostrar los nombres de proveedores tales que el total de sus ventas superen la cantidad de 1000 unidades.
SELECT p.nompro, SUM(v.cantidad) FROM proveedor p, ventas v
WHERE v.codpro = p.codpro
GROUP BY p.nompro

--Ejercicio 3.36 Mostrar la pieza que más se ha vendido en total.
SELECT p.nompie, sum(v.cantidad)
FROM ventas v, pieza p
where p.codpie = v.codpie
GROUP BY p.nompie
HAVING SUM(cantidad) = (SELECT MAX(SUM(V1.cantidad))
FROM ventas V1
GROUP BY V1.codpie);

--Ejercicio 3.38 Encontrar la cantidad media de piezas suministradas cada mes.
SELECT TO_CHAR(fecha,'MM') AS mes, ROUND(AVG(cantidad), 2) AS media
FROM ventas
GROUP BY TO_CHAR(fecha,'MM')
ORDER BY mes ASC

--Ejercicio 3.42 Mostrar los códigos de aquellos proveedores que hayan superado las ventas totales realizadas por el proveedor ’S1’
SELECT codpro FROM ventas
GROUP BY codpro
HAVING SUM(cantidad) > (SELECT SUM(V1.cantidad) FROM ventas V1 
WHERE v1.codpro = 'S1'
GROUP BY V1.codpro)

--Ejercicio 3.43 Mostrar los mejores proveedores, entendiéndose como los que tienen mayores
cantidades totales.
--(no se a cuantos se refiere cuándo dice mostrar los mejores, por lo que en la primera opción muestro los proveedores ordenados de mayor a menor cantidad y en el segundo muestra el que más ha vendido)
SELECT codpro FROM ventas
GROUP BY codpro
ORDER BY SUM(cantidad) DESC
-----------------------------------------------------------------------
SELECT codpro FROM ventas
GROUP BY codpro
HAVING SUM(cantidad) = (SELECT MAX(SUM(V1.cantidad)) FROM ventas V1 GROUP BY V1.codpro)


--Ejercicio 3.45 Encontrar aquellos proveedores que hayan hecho al menos diez pedidos.
SELECT codpro FROM ventas
GROUP BY codpro
HAVING COUNT(cantidad) >= 10;

--Ejercicio 3.52 Mostrar para cada proveedor la media de productos suministrados cada año.
SELECT codpro, AVG(cantidad) media, TO_CHAR(fecha,'yyyy') año
FROM ventas
GROUP BY codpro, TO_CHAR(fecha,'yyyy')
ORDER BY codpro, año

--Ejercicio 3.54 Encontrar todos los proveedores que venden todas las piezas rojas.
SELECT p.codpro
FROM proveedor p
WHERE EXISTS (
    SELECT p1.codpie
    FROM pieza p1
    WHERE p1.color = 'Rojo'
    AND EXISTS (
        SELECT v.codpie
        FROM ventas v
        WHERE v.codpro = p.codpro and v.codpie = p1.codpie
    )
)

--Ejercicio 3.55 Encontrar todos los proveedores tales que todas las piezas que venden son rojas.
SELECT p1.codpro
FROM proveedor p1
WHERE NOT EXISTS (
    SELECT v.codpro
    FROM ventas v, pieza pie
    WHERE v.codpie = pie.codpie and p1.codpro = v.codpro and pie.color<> 'Rojo'
)

--Ejercicio 3.56 Encontrar el nombre de aquellos proveedores que venden más de una pieza roja.
SELECT p.nompro,COUNT(p.nompro)
FROM proveedor p, pieza pie, ventas v 
WHERE p.codpro = v.codpro and pie.codpie = v.codpie and pie.color = 'Rojo'
GROUP BY p.nompro
HAVING COUNT(p.nompro) > 1

--Ejercicio 3.57 Encontrar todos los proveedores que vendiendo todas las piezas rojas cumplen la condición de que todas sus ventas son de más de 10 unidades.
SELECT p.codpro
FROM proveedor p
WHERE EXISTS (
    SELECT p1.codpie
    FROM pieza p1
    WHERE p1.color = 'Rojo'
    AND EXISTS (
        SELECT v.codpie
        FROM ventas v
        WHERE v.codpro = p.codpro and v.codpie = p1.codpie
    )
)
AND NOT EXISTS (
    SELECT v2.codpie
    FROM ventas v2
    WHERE v2.codpro = p.codpro AND v2.cantidad <= 10
);

--Ejercicio 3.58 Coloca el status igual a 1 a aquellos proveedores que sólo suministran la pieza P1.
UPDATE proveedor p
SET status = 1
WHERE NOT EXISTS(
    SELECT v.codpie
    FROM ventas v
    WHERE v.codpro = p.codpro
    AND EXISTS (
        SELECT pie.codpie
        FROM pieza pie
        WHERE pie.codpie = v.codpie and v.codpie <> 'P1'
    )
)








----------------------------------------------------------------------------------------------
---------------------EJERCICIOS LIGA DE BALONCESTO--------------------------------------------
----------------------------------------------------------------------------------------------


--Ejercicio 3.60 Muestra la información disponible acerca de los encuentros de liga.
SELECT * FROM encuentros

--Ejercicio 3.61 Muestra los nombres de los equipos y de los jugadores jugadores ordenados alfabéticamente.
SELECT nombree FROM equipos
UNION
SELECT nombreJ FROM Jugadores
ORDER BY nombree;

--Ejercicio 3.62 Muestra los jugadores que no tienen ninguna falta.
(SELECT codj
FROM jugadores)
MINUS
(SELECT codj
FROM faltas)

--Ejercicio 3.63 Muestra los compañeros de equipo del jugador que tiene por código x (codJ=’x’) y donde x es uno elegido por ti.
(SELECT codj FROM jugadores
WHERE codj LIKE 'A%')
MINUS
(SELECT codj FROM jugadores
WHERE codj = 'A2')

--Ejercicio 3.64 Muestra los jugadores y la localidad donde juegan (la de sus equipos).
SELECT j.codj, e.localidad FROM equipos e, jugadores j
WHERE j.code = e.code


--3.65 Muestra todos los encuentros posibles de la liga.
SELECT e1.nombree,e2.nombree 
FROM equipos e1, equipos e2
WHERE e1.code<>e2.code

--Ejercicio 3.66 Muestra los equipos que han ganado algún encuentro jugando como local. 
SELECT DISTINCT eq.code
FROM encuentros e, equipos eq
WHERE eq.code = e.elocal and e.plocal > e.pvisitante

--Ejercicio 3.67 Muestra los equipos que han ganado algún encuentro.
SELECT distinct eq.code
FROM encuentros e, equipos eq
WHERE (eq.code = e.elocal and e.plocal > e.pvisitante) OR (eq.code = e.evisitante and e.plocal < e.pvisitante)

--Ejercicio 3.68 Muestra los equipos que todos los encuentros que han ganado lo han hecho como equipo local.
(SELECT DISTINCT eq.code
FROM encuentros e, equipos eq
WHERE eq.code = e.elocal and e.plocal > e.pvisitante)
MINUS 
(SELECT DISTINCT eq.code
FROM encuentros e, equipos eq
WHERE eq.code = e.evisitante and e.plocal < e.pvisitante)

--Ejercicio 3.69 Muestra los equipos que han ganado todos los encuentros jugando como equipo local.
(SELECT DISTINCT eq.code
FROM encuentros e, equipos eq
WHERE eq.code = e.elocal and e.plocal > e.pvisitante)
MINUS 
(SELECT DISTINCT eq.code
FROM encuentros e, equipos eq
WHERE eq.code = e.elocal and e.plocal < e.pvisitante)

--Ejercicio 3.70 Muestra los encuentros que faltan para terminar la liga. Suponiendo que en la Encuentros sólo se almacenan los encuentros celebrados hasta la fecha.
(SELECT e1.nombree,e2.nombree 
FROM equipos e1, equipos e2
WHERE e1.code<>e2.code)
MINUS
(SELECT e1.nombree,e2.nombree 
FROM equipos e1, equipos e2, encuentros e
WHERE (e1.code = e.elocal and e2.code = e.evisitante))

--Ejercicio 3.71 Muestra los encuentros que tienen lugar en la misma localidad.
--no estoy seguro de si es lo que he hecho, muestra los equipos que van a jugar sus dos partidos en la misma localidad
SELECT e1.nombree local,e2.nombree visitante, e1.localidad
FROM equipos e1, equipos e2
WHERE e1.code<>e2.code and (e1.localidad = e2.localidad)
ORDER BY e1.localidad

--Ejercicio 3.72 Para cada equipo muestra cantidad de encuentros que ha disputado como local.
SELECT e.code, COUNT(ec.elocal)
FROM equipos e, encuentros ec
WHERE e.code = ec.elocal and ec.plocal > ec.pvisitante
GROUP BY e.code

--Ejercicio 3.73 Muestra los encuentros en los que se alcanzó mayor diferencia.
--partido en el que más
SELECT eq1.nombree, eq2.nombree, ABS(e.plocal-e.pvisitante) AS diferencia
FROM encuentros e, equipos eq1,equipos eq2
WHERE e.elocal = eq1.code and e.evisitante = eq2.code and ABS(plocal-pvisitante) = (SELECT MAX(ABS(e1.plocal-e1.pvisitante)) FROM encuentros e
--lista de partidos ordenada por diferencia
SELECT distinct eq1.nombree, eq2.nombree, ABS(e.plocal-e.pvisitante) AS diferencia
FROM encuentros e, equipos eq1,equipos eq2
WHERE e.elocal = eq1.code and e.evisitante = eq2.code
ORDER BY diferencia DESC

--Ejercicio 3.74 Muestra los jugadores que no han superado 3 faltas acumuladas.
--muestra el cod de todos los jugadores con 3 o menos faltas
(SELECT codj
FROM jugadores)
MINUS
(SELECT j.codj
FROM faltas f, jugadores j
WHERE j.codj = f.codj
GROUP BY j.codj
HAVING SUM(f.num) > 3
)

--Ejercicio 3.75 Muestra los equipos con mayores puntuaciones en los partidos jugados fuera de casa.
SELECT eq.code, e.pvisitante
FROM encuentros e, equipos eq
WHERE e.evisitante = eq.code
ORDER BY e.pvisitante DESC
---------------------------------
--este muestra solo el que más tiene
SELECT eq.code, e.pvisitante
FROM encuentros e, equipos eq
WHERE e.evisitante = eq.code  and e.pvisitante = (SELECT MAX(e1.pvisitante) FROM encuentros e1)
ORDER BY e.pvisitante DESC

--Ejercicio 3.76 Muestra la cantidad de victorias de cada equipo, jugando como local o como visitante.
SELECT e.code, e.nombree, 
    (SELECT COUNT(enc1.elocal)
    FROM encuentros enc1
    WHERE enc1.elocal = e.code and enc1.plocal > enc1.pvisitante
    ) AS victorias_local,
    (SELECT COUNT(enc2.evisitante)
    FROM encuentros enc2
    WHERE enc2.evisitante = e.code and enc2.plocal < enc2.pvisitante
    ) AS victorias_visitante

FROM equipos e

--Ejercicio 3.77 Muestra el equipo con mayor número de victorias.
SELECT eq.code,
    (SELECT COUNT(enc1.elocal)
    FROM encuentros enc1
    WHERE enc1.elocal = eq.code and enc1.plocal > enc1.pvisitante
    )+
    (SELECT COUNT(enc2.evisitante)
    FROM encuentros enc2
    WHERE enc2.evisitante = eq.code and enc2.plocal < enc2.pvisitante
    ) AS vicTotal

FROM equipos eq
GROUP BY eq.code
ORDER BY vicTotal DESC
FETCH FIRST 1 ROW ONLY

--Ejercicio 3.78 Muestra el promedio de puntos por equipo en los encuentros de ida.
SELECT eq.code, ROUND(AVG(e.plocal), 2) AS promedio_puntos
FROM equipos eq, encuentros e
WHERE eq.code = e.elocal
GROUP BY eq.code

--Ejercicio 3.79 Muestra el equipo con mayor número de puntos en total de los encuentros jugados.
SELECT e.code,
    (SELECT SUM(enc1.plocal)
    FROM encuentros enc1
    WHERE e.code = enc1.elocal
    )+ 
    (SELECT SUM(enc2.pvisitante)
    FROM encuentros enc2
    WHERE e.code = enc2.evisitante
    ) AS ptos_tot


FROM equipos e
GROUP BY e.code
ORDER BY ptos_visit DESC NULLS LAST
FETCH FIRST 1 ROW ONLY




----------------------------------------------------------------------------------------------
-----------------------------EJERCICIOS APARTADO 4--------------------------------------------
----------------------------------------------------------------------------------------------


--Ejercicio 4.1 Crear una vista con los proveedores de Londres. ¿Qué sucede si insertamos en dicha vista la tupla (’S7’,’Jose Suarez’,3,’Granada’)?
CREATE VIEW proveedores_londres AS
SELECT * FROM proveedor
WHERE proveedor.ciudad = 'Londres';

INSERT INTO proveedores_londres 
    VALUES('S7','Jose Suarez',3,'Granada')
--da error ya que no cumple la restricción solicitada


--Ejercicio 4.2 Crear una vista con los nombres de los proveedores y sus ciudades. Inserta sobre ella una fila y explica cuál es el problema que se plantea. ¿Habría problemas de actualización?
CREATE VIEW ciu_pro AS 
    SELECT nompro, ciudad
    FROM proveedor;
INSERT INTO ciu_pro 
    VALUES('Manolo', 'Granada');
--No me deja añadir valores ya que no deja insertar valores nulos en codpro


----------------------------------------------------------------------------------------------
-----------------------------EJERCICIOS APARTADO 5--------------------------------------------
----------------------------------------------------------------------------------------------






















