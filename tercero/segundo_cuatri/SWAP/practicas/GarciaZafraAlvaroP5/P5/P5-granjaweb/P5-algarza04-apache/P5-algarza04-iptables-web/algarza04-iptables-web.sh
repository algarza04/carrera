#!/bin/bash

# Establecemos una política de denegación implícita de todo el tráfic
# Descartamos cualquier paquete que no cumpla con una regla explícita
# el parámetro -P establece la política por defecto de las cadenas INPUT, OUTPUT y FORWARD
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Permitir que las respuestas iniciadas por localhost se acepten
# el parámetro -A agrega una regla
# -m state permite filtrar paquetes establecidos(ESTABLISHED) y relacionados(RELATED) a una conexión
# -j ACCEPT indica que se acepten los paquetes que cumplan lo anterior
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Permitir que localhost inicie y mantenga conexiones sin interrupción
# los parámetros de esta regla son los mismos que la anterior pero para OUTPUT
iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

# Permitir el tráfico que el host se envía a sí mismo
# en cada uno añadimos una regla (INPUT/OUTPUT) para aceptar el tráfico del localhost(-i input, -o output)
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Permitior el tráfico TCP entrante al puerto 80 y 443 si proviene del balanceador
# Añadimos una regla para el protocolo TCP, solo si viene de 192.168.19.50 
# -dport indica el puerto de destino
iptables -A INPUT -p tcp -s 192.168.10.50 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -s 192.168.10.50 --dport 443 -j ACCEPT



