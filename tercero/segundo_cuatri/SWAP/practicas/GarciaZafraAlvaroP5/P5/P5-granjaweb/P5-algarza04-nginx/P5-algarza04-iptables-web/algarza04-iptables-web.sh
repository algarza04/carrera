#!/bin/bash

# Si una IP establece más de 10 conexiones en 10 segundos, se la bloquea temporalmente.
iptables -A INPUT -p tcp --dport 80 -m recent --name ddos --update --seconds 10 --hitcount 10 -j DROP
iptables -A INPUT -p tcp --dport 80 -m recent --name ddos --set
iptables -A INPUT -p tcp --dport 443 -m recent --name ddos --update --seconds 10 --hitcount 10 -j DROP
iptables -A INPUT -p tcp --dport 443 -m recent --name ddos --set

# Protección personalizada contra DDoS
# Crear la nueva cadena 
iptables -N DDOS-PROTECT

# Detectar IPs que abusan de nuevas conexiones
iptables -A DDOS-PROTECT -m recent --name badguy --rcheck --seconds 60 -j DROP

# Eliminar IPs que han hecho más de 15 conexiones en 60 segundos
iptables -A DDOS-PROTECT -m recent --name badguy --update --seconds 60 --hitcount 15 -j DROP

# Aplicar la cadena al tráfico entrante
iptables -A INPUT -p tcp --dport 80 -j DDOS-PROTECT
iptables -A INPUT -p tcp --dport 443 -j DDOS-PROTECT

# Limitar conexiones simultáneas para cada IP por el puerto 80 (HTTP) y 443 (HTTPS)
iptables -A INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 10 --connlimit-mask 32 -j REJECT --reject-with tcp-reset
iptables -A INPUT -p tcp --syn --dport 443 -m connlimit --connlimit-above 10 --connlimit-mask 32 -j REJECT --reject-with tcp-reset

# Bloquear escaneo de puertos (port scanning)
iptables -N PORTSCAN
iptables -A PORTSCAN -p tcp --tcp-flags SYN,ACK,FIN,RST RST -m limit --limit 1/s --limit-burst 2 -j RETURN
iptables -A PORTSCAN -j DROP
iptables -A INPUT -p tcp --tcp-flags SYN,ACK,FIN,RST RST -j PORTSCAN

# Permitir solo puertos necesarios
iptables -P INPUT DROP
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

