#!/bin/bash

# Ejecuta el comando de Apache Benchmark (ab) para realizar pruebas de carga
# Mandará 10000 peticiones con una concurrencia de 100 tanto a HTTPS como a HTTP
ab -n 10000 -c 100 https://192.168.10.50:443/
ab -n 10000 -c 100 http://192.168.10.50:80/

# Luego, ejecuta el comando principal del contenedor
exec "$@"

