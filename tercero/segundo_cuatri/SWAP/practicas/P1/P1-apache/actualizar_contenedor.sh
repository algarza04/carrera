#!/bin/bash

containers=$(docker ps -q)	#containers contendrá las IP de todos los contenedores cuyo status sea up

for container in $containers; do	
	docker exec -u root $container bash -c "apt update && apt upgrade -y"
done
#este for irá recorriendo uno a uno todos los contenedores y actualizará cada uno el -u root es porque necesita permisos para poder realizar esto, por lo que accedemos como root, nos metemos en la terminal y ejecutamos ambos comandos

echo "Contenedores actualizados"
