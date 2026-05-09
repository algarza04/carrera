#!/bin/bash

# Obtener todos los contenedores en ejecución
containers=$(docker ps -q)

# Verifica si hay contenedores en ejecución, en el caso de que no haya finalizará
if [ -z "$containers" ]; then
    echo "No hay contenedores en ejecución."
    exit 1
fi

# En el caso de que si haya los detendrá con la orden docker stop
echo "Deteniendo todos los contenedores..."
docker stop $containers

echo "Todos los contenedores han sido detenidos."
