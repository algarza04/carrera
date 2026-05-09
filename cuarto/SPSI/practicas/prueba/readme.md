#

## Generación de claves

En primer lugar obtenemos las parejas de llaves publica/privada
`openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:3 -out privkey-ID.pem`

para ver los valores individuales de la clave privada:
`openssl pkey -in privkey-ID.pem -text`
esto último muestra el contenido que pudimos ver con cat y + param...

generación de su clave pública compañear y volcado en el fichero
`openssl pkey -in privkey-ID.pem -out pubkey-ID.pem -pubout`

ver los valores de la clave pública:
`openssl pkey -in pubkey-ID.pem -pubin -text`

emisor:
`openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:3 -out privkey-userS.pem`
`openssl pkey -in privkey-userS.pem -out pubkey-userS.pem -pubout`

receptor:
`openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -pkeyopt rsa_keygen_pubexp:5 -out privkey-userR.pem`
`openssl pkey -in privkey-userR.pem -out pubkey-userR.pem -pubout`

una vez hecho esto podemos realizar el intercambio de claves públicas


Es preciso cuidarse mucho de la coincidencia en los exponentes (p.e. tres usuarios con
exponente 3) pues ello podría comprometer las comunicaciónes del círculo.

## PASOS EMISOR
El primer paso a realizar es firmar el mensaje con la huella hash
`openssl dgst -sha256 -sign privkey-userS.pem -out message-userS.txt.sgn message-userS.txt`

ciframos el mensaje con rsa para que terceros no puedan leer el mensaje, para esto usamos la clave pública del que será el receptor del mensaje
`openssl pkeyutl -encrypt -in message-userS.txt -pubin -inkey pubkey-userR.pem -out message-userS.txt.enc`

Obsérvese que el cifrado con RSA debería ser usado con ficheros pequeños, con longitud
menor a la de un resumen. Si es preciso cifrar mensajes largos, deberá usar cifras
simétrica.

Enviamos la pareja de ficheros que hemos cifrado message-userS.txt.sgn y message-
userS.txt.enc

## PASOS RECEPTOR
El primer paso del receptor es descifrar el mensaje
`openssl pkeyutl -decrypt -in message-userS.txt.enc -inkey privkey-userR.pem -out rec-message-userS.txt`

Para asegurarse de que el mensaje ha recibido de quien dice ser el emisario:
`openssl dgst -sha256 -verify pubkey-userS.pem -signature message-userS.txt.sgn rec-message-userS.txt`






echo Le ruego que disponga de 15540.40 dólares de mi cuenta, a la que tiene acceso, para adquirir para mí un Bitcoin > message-userS.txt