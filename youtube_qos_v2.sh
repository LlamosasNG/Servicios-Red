#!/bin/bash

# youtube_qos.sh
NOMBRE_SCRIPT="acl_youtube_qos"
NUMERO_ACL=1
CLASS_MAP_NAME="YOUTUBE_TRAFFIC"
POLICY_MAP_NAME="YOUTUBE_LIMIT_POLICY"
BANDWIDTH_LIMIT=50000  # 50,000 bps

# Eliminamos configuraciones previas si existen
echo "no access-list $NUMERO_ACL" > /tmp/$NOMBRE_SCRIPT
echo "no class-map $CLASS_MAP_NAME" >> /tmp/$NOMBRE_SCRIPT
echo "no policy-map $POLICY_MAP_NAME" >> /tmp/$NOMBRE_SCRIPT

# Obtenemos todas las direcciones IP del dominio www.youtube.com
dig www.youtube.com +short | while read IP; do
    if [[ $IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "access-list $NUMERO_ACL permit host $IP" >> /tmp/$NOMBRE_SCRIPT
    fi
done

# Obtenemos todas las direcciones IP del dominio youtube.com
dig youtube.com +short | while read IP; do
    if [[ $IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "access-list $NUMERO_ACL permit host $IP" >> /tmp/$NOMBRE_SCRIPT
    fi
done

# Obtenemos todas las direcciones IP del dominio youtube-ui.l.google.com
dig youtube-ui.l.google.com +short | while read IP; do
    if [[ $IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "access-list $NUMERO_ACL permit host $IP" >> /tmp/$NOMBRE_SCRIPT
    fi
done

# Agregamos rangos adicionales conocidos de YouTube/Google
echo "access-list $NUMERO_ACL permit 208.65.152.0 0.0.7.255" >> /tmp/$NOMBRE_SCRIPT
echo "access-list $NUMERO_ACL permit 208.117.224.0 0.0.31.255" >> /tmp/$NOMBRE_SCRIPT
echo "access-list $NUMERO_ACL permit 74.125.0.0 0.0.255.255" >> /tmp/$NOMBRE_SCRIPT

# Configuración del Class-Map para identificar tráfico de YouTube
cat << 'CLASSMAP' >> /tmp/$NOMBRE_SCRIPT
!
! Configuración del Class-Map
class-map match-all YOUTUBE_TRAFFIC
match access-group 1
match protocol ip
!
CLASSMAP

# Configuración del Policy-Map para limitar ancho de banda
cat << POLICYMAP >> /tmp/$NOMBRE_SCRIPT
!
! Configuración del Policy-Map
policy-map $POLICY_MAP_NAME
class $CLASS_MAP_NAME
police rate $BANDWIDTH_LIMIT bps burst 8000 byte exceed-action drop
class class-default
fair-queue
!
POLICYMAP

# g1/0 - INPUT: Tráfico entrante desde R2/Internet (aquí limitamos YouTube)
echo "interface g1/0" >> /tmp/$NOMBRE_SCRIPT
echo "service-policy input $POLICY_MAP_NAME" >> /tmp/$N OMBRE_SCRIPT

# g0/0 - OUTPUT: Tráfico saliente hacia PCs ( para control adicional)
echo "interface g0/0" >> /tmp/$NOMBRE_SCRIPT
echo "service-policy output $POLICY_MAP_NAME" >> /tmp/$NOMBRE_SCRIPT

echo "end" >> /tmp/$NOMBRE_SCRIPT
echo "write memory" >> /tmp/$NOMBRE_SCRIPT

# Resto del script igual...
echo "=== Configuración generada ==="
cat /tmp/$NOMBRE_SCRIPT
echo "=============================="


# Ejecutamos los comandos de configuración utilizando SSH sin contraseña
# Nota: Ajusta la IP según la interfaz de gestión del Router 2
# Basándome en la topología, asumo que te conectas via la red 3.5.100.0/24
echo "Aplicando configuración en Router 2..."

ssh -T -o PreferredAuthentications=publickey -o Ciphers=aes128-cbc admin3@3.5.100.11 << EOF
configure terminal
$(cat /tmp/$NOMBRE_SCRIPT)
EOF

# Verificamos la configuración aplicada
echo "Verificando configuración aplicada..."
ssh -T -o PreferredAuthentications=publickey -o Ciphers=aes128-cbc admin3@3.5.100.11 << 'VERIFY'
show access-lists 1
show class-map YOUTUBE_TRAFFIC
show policy-map YOUTUBE_LIMIT_POLICY
show policy-map interface g0/0
show policy-map interface g1/0
VERIFY

echo "Script completado. Revisa la salida para confirmar la configuración."