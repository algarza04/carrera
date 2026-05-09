///EXAMEN 2018 

EJERCICIO 1
  CREATE TABLE PEDIDO(
    Ped# varchar2(8) PRIMARY KEY, 
    F_P date CHECK (To_number(To_char(F_P, 'yyyy')) > 2009), 
    F_E date CHECK (To_number(To_char(F_P, 'yyyy')) > 2009), 
    F_r date CHECK (To_number(To_char(F_P, 'yyyy')) > 2009), 
    email NOT NULL REFERENCES Usuario(email),
    Pago# NOT NULL REFERENCES Met_pago(Pago#), 
    CHECK ‌F_P<=F_E<=F_R
  )

  CREATE TABLE CHEQUE(
    Disponible NUMBER CHECK (Disponible >= 0), 
    Cheque# PRIMARY KEY REFERENCES Met_Pago(Pago#), 
    Tarjeta# NOT NULL REFERENCES Tarjeta(Tarjeta#),
    CHECK(Cheque#<>Tarjeta#)
  )


EJERCICIO 2
Mostrar‌ ‌los‌ ‌nombres‌ ‌de‌ ‌los‌‌ usuarios‌‌ que‌‌ hayan‌‌ pedido‌‌ todos‌‌ los‌‌ artículos‌‌ cuyo‌‌ precio‌‌ unitario‌‌ e s‌‌inferior‌‌a‌‌ 20e.‌ 
  
  π Usuario.nombre, Ref# (Usuario⨝Pedido⨝Incluye)) ÷ π Ref# (σ Precio<20 (Articulo)) 
  SELECT nombre FROM Usuario 
  WHERE NOT EXISTS(
  (SELECT Ref# FROM Articulo WHERE Precio<20) 
  MINUS 
  (SELECT Ref# FROM Usuario NATURAL JOIN pedido NATURAL JOIN incluye WHERE pedido.email=Usuario.email ))
  
  
EJERCICIO 3
Mostrar‌ ‌el‌ ‌código‌ ‌del‌ ‌pedido‌ ‌junto‌ ‌con‌ ‌su‌ ‌importe‌ ‌total,‌ ‌de‌ ‌aquellos‌ ‌pedidos‌ ‌cuyo‌‌ importe‌‌ total‌‌ sea‌‌ mayor‌‌ que‌‌ 1000‌‌e,‌‌ ordenados‌‌ por‌‌ importe‌‌ total.

  SELECT Ped, Sum(Cantidad*precio) as total
  FROM Incluye, Articulo
  WHERE Incluye.Ref=Articulo.Ref
  GROUP BY Ped HAVING Sum(Cantidad*precio)>1000
  ORDER BY total


EJERCICIO 4
Mostrar‌‌ los‌‌ datos‌‌ del‌‌ pedido‌‌ más‌‌ antiguo.

  π Ped#, F_P (Pedido) - π Pedido.Ped#, F_P (σ F_P>P.F_P (Pedido ⨯ ρ P Pedido))
