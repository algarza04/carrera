CREATE TABLE pedido (
    Ped# varchar2(8) PRIMARY KEY,
    F_P date CHECK(TO_NUMBER(to_char(F_P,'YYYY')) > 2009),
    F_E date, 
    F_R date,
    email NOT NULL REFERENCES Usuario(email),
    Pago# NOT NULL REFERENCES Met_Pago(Pago#),
    CHECK (F_P<=F_E AND F_E<=F_R)
);

CREATE TABLE Cheque(
    Cheque# PRIMARY KEY REFERENCES Met_Pago(Pago#),
    Tarjeta# NOT NULL REFERENCES Tarjeta(Tarjeta#),
    Disponible NUMBER CHECK(Disponible >= 0), 
    CHECK(Cheque#<>Tarjeta#)
);

--Mostrar‌ ‌los‌ ‌nombres‌ ‌de‌ ‌los‌‌usuarios‌‌que‌‌hayan‌‌pedido‌‌todos‌‌los‌‌artículos‌‌cuyo‌‌precio‌‌
unitario‌‌es‌‌inferior‌‌a‌‌20e.
πnombre(Usuario⨝(πemail, ref# (pedido⨝incluye) ÷ πref#(σ precio<20(articulo))
SELECT u.nombre 
FROM usuario U
WHERE NOT EXISTS (
    (SELECT ref# FROM articulo 
    where precio<20 
    )
    MINUS
    (SELECT i.ref# 
    FROM Incluye i NATURAL JOIN Pedido p 
    WHERE i.ped# = p.ped# and p.email = u.email
    )
);

--Mostrar‌ ‌el‌ ‌código‌ ‌del‌ ‌pedido‌ ‌junto‌ ‌con‌ ‌su‌ ‌importe‌ ‌total,‌ ‌de‌ ‌aquellos‌ ‌pedidos‌ ‌cuyo‌‌ 
--importe‌‌total‌‌sea‌‌mayor‌‌que‌‌1000‌‌e,‌‌ordenados‌‌por‌‌importe‌‌total.‌(‌ SQL‌‌1.75‌‌ptos)‌ ‌
SELECT i.ped#, SUM(a.precio * i.cantidad) as importe_total
FROM incluye i, articulo a
WHERE i.ref# = a.ref#
GROUP BY i.ped#
HAVING SUM(a.precio*i.cantidad) > 1000
order by importe_total

--Mostrar‌‌los‌‌datos‌‌del‌‌pedido‌‌más‌‌antiguo.‌
ρ(Pedido) = P1,P2
(Pedido ⨝(πped# (P1)- πP1.ped#(σP1.F_P >P2.F_P (P1 × P2)))
