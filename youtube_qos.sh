NOMBRE_SCRIPT="acl_youtube"
NUMERO_ACL=1

# eliminamos la lista de control de acceso 1 (si acaso existe)
echo "no access-list $NUMERO_ACL" > /tmp/$NOMBRE_SCRIPT

# obtenemos todas las direcciones IP de YouTube y las incluimos en el comando access-list
dig www.youtube.com +short | while read IP; do
  echo "access-list $NUMERO_ACL permit host $IP" >> /tmp/$NOMBRE_SCRIPT
done
dig youtube.com +short | while read IP; do
  echo "access-list $NUMERO_ACL permit host $IP" >> /tmp/$NOMBRE_SCRIPT
done
dig youtube-ui.l.google.com +short | while read IP; do
  echo "access-list $NUMERO_ACL permit host $IP" >> /tmp/$NOMBRE_SCRIPT
done

# agregamos la regla para permitir cualquier otro tráfico
echo "access-list $NUMERO_ACL permit any" >> /tmp/$NOMBRE_SCRIPT

# Comandos para crear class-map, policy-map y aplicar el service-policy
cat << 'EOF_CM' >> /tmp/$NOMBRE_SCRIPT
!
class-map match-any youtube
 match access-group 1
!
policy-map Limit-Youtube
 description To Limit YOUTUBE traffic
 class youtube
  police cir 50000
   conform-action transmit
   exceed-action drop
!
interface Gi0/0
 service-policy output Limit-Youtube
!
EOF_CM

# ejecutamos los comandos de configuración utilizando SSH
ssh -T -o PreferredAuthentications=publickey -o Ciphers=aes128-cbc admin3@3.5.100.11 << EOF
configure terminal
$(cat /tmp/$NOMBRE_SCRIPT)
end
EOF