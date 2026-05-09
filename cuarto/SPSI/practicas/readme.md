# 
El objetivo es obtener una clave secreta compartida entre dos usuarios.
Vamos a utilizar una AC para evitar la actividad de un tercero.

Utilizamos aritmética modular y exponenciales, el cuál es imposible de resolver con valores suficientemente grandes.


### usuario1
openssl genpkey -genparam -algorithm DH -out dhp.pem

observar salida
openssl pkeyparam -in dhp.pem -text

manda el fichero .pem


openssl genpkey -paramfile dhp.pem -out dhkey1.pem

si queremos ver el contenido
openssl pkey -in dhkey1.pem -text -noout

obtención de claves públicas
openssl pkey -in dhkey1.pem -pubout -out dhpub1.pem

ver su contenido
openssl pkey -pubin -in dhpub1.pem -text

### usuario 2
openssl genpkey -paramfile dhp.pem -out dhkey2.pem

si queremos ver el contenido
openssl pkey -in dhkey2.pem -text -noout


obtención de claves públicas
openssl pkey -in dhkey2.pem -pubout -out dhpub2.pem

ver su contenido
openssl pkey -pubin -in dhpub2.pem -text


## Obtención de secreto compartido
### usuario1
openssl pkeyutl -derive -inkey dhkey1.pem -peerkey dhpub2.pem -out secret1.bin

### usuario 2
openssl pkeyutl -derive -inkey dhkey2.pem -peerkey dhpub1.pem -out secret2.bin


comparar 
diff secret1.bin secret2.bin
o
cmp secret1.bin secret2.bin

o
xxd secret1.bin
xxd secret2.bin

## Ejemplo de uso
