#!/bin/bash

# Ejecuta el script de iptables
./algarza04-iptables-web.sh

# Luego, ejecuta el comando principal del contenedor
exec "$@"

