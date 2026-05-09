//ENTREGA SESION 10

EJERICICO 1

CREATE TABLE Barcos(
  NomBarco varchar2(32) PRIMARY KEY,
  NomClase REFERENCES Clase(NomClase), 
  FechaCons date, 
  Pais varchar2(10)
);

CREATE TABLE Clase(
  NomClase varchar2(32) CHECK (NomClase in ('Goleta', 'Carabela', 'Fragata', 'Galeón')) PRIMARY KEY,
  Tipo varchar2(32), 
  NCanones NUMBER DEFAULT(4), 
  Calibre NUMBER,
  Tonelaje NUMBER NOT NULL
);

CREATE TABLE Batalla(
  NomBatalla varchar2(32) PRIMARY KEY,
  Localizacion varchar2(32)
);

CREATE TABLE Participa(
  NomBatalla varchar2(32) REFERENCES Batalla(NomBatalla),
  NomBarco varchar2(32) REFERENCES Barcos(NomBarco),
  Estado varchar2(32) CHECK (Estado in ('Hundido', 'Indemne', 'Perjudicao')), 
  PRIMARY KEY(NomBatalla, NomBarco)
);


EJERCICIO 2 AR-SQL

  π NomBarco (σ NomClase='Goleta' (Barcos)) - π NomBarco (σ NomClase='Goleta' ∧     Participa.NomBarco=P.NomBarco ∧ Participa.NomBatalla!=P.NomBatalla ((Participa ⨯ ρ P Participa)⨝ Barcos))
  
  SELECT NomBarco, count(*) as numBatallas
  FROM Participa NATURAL JOIN BarcosS
  WHERE NomClase='Goleta'
  GROUP BY NomBarcos HAVING count(*)=1


EJERCICIO 3
  
 π NomBatalla, Localizacion (π NomBatalla, NomBarco (σ Localizacion='Pacifico' (Participa ⨝ Batalla)) ÷ π NomBarco (σ Ncanones>10 (Barcos⨝Clase))⨝Batallas)
  
  SELECT NomBatalla, Localizacion FROM Batalla WHERE NOT EXISTS(
    (SELECT NomBarco FROM Barcos NATURAL JOIN Clase WHERE Ncanones>10)
    MINUS
    (SELECT NomBarco Participa NATURAL JOIN Batalla WHERE Localizacion='Pacifico' AND Participa.NomBatalla = Batalla.NomBatalla) 
  )
  

EJERCICIO 4

  SELECT NomBatalla, Count(*) as contador
  WHERE Estado='HUNDIDO'
  FROM Participa 
  GROUP BY NomBatalla HAVING Count(*)>10


EJERCICIO 5
  
  CREATE VIEW AS (
	SELECT Pais, Count(*) as Contador, to_char(FechaCons, 'YYYY') as anio
	FROM Barcos 
	GROUP BY pais, to_char(FechaCons, 'YYYY')
  )
