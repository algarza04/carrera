#!/bin/bash

# Consultar las métricas de Prometheus para obtener el uso de CPU de los contenedores web
cpu_usage=$(curl -s "http://localhost:9090/api/v1/query?query=avg(rate(container_cpu_usage_seconds_total{container_name=~'web.*'}[1m]))" | jq '.data.result[0].value[1]')

# Establecer un umbral de CPU para escalar
umbral_cpu=0.75  # Si la CPU promedio es mayor al 75%, escalamos

# Decidir el número de instancias basado en la carga de CPU
if (( $(echo "$cpu_usage > $umbral_cpu" | bc -l) )); then
  echo "La carga de CPU es alta ($cpu_usage). Escalando a más instancias..."
  docker-compose up --scale web=12 -d  # Aumentamos las instancias de web
else
  echo "La carga de CPU es baja ($cpu_usage). No se necesita escalar."
fi

