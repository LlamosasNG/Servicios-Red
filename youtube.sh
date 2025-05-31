# youtube.sh
# Carlos Pineda G. 2024
NOMBRE_SCRIPT="acl_youtube"
NUMERO_ACL=1
# eliminamos la lista de control de acceso 1 (si acaso existe)
echo "no access-list $NUMERO_ACL" > /tmp/$NOMBRE_SCRIPT
# obtenemos todas las direcciones IP del dominio www.youtube.com y 
# las incluimos en el comando access-list
dig www.youtube.com +short | while read IP; do
echo "access-list $NUMERO_ACL deny host $IP" >> /tmp/$NOMBRE_SCRIPT
done
# obtenemos todas las direcciones IP del dominio youtube.com y 
# las incluimos en el comando access-list
dig youtube.com +short | while read IP; do
echo "access-list $NUMERO_ACL deny host $IP" >> /tmp/$NOMBRE_SCRIPT
done
# obtenemos todas las direcciones IP del dominio youtube-ui.l.google.com y 
# las incluimos en el comando access-list
dig youtube-ui.l.google.com +short | while read IP; do
echo "access-list $NUMERO_ACL deny host $IP" >> /tmp/$NOMBRE_SCRIPT
done
# agregamos la regla para cancelar la denegación implícita de todo
echo "access-list $NUMERO_ACL permit any" >> /tmp/$NOMBRE_SCRIPT
# asignamos la lista de control de acceso a la salida de la interfce 
# Gi1/0 del router R1
echo "interface Gi1/0" >> /tmp/$NOMBRE_SCRIPT
echo "ip access-group $NUMERO_ACL out" >> /tmp/$NOMBRE_SCRIPT
# ejecutamos los comandos de configuración utilizando SSH sin contraseña
# en este caso el usuario es admin2 y la dirección IP de la interface que 
# usamos para conectarnos al router R1 es 3.5.200.10
ssh -T -o PreferredAuthentications=publickey -o Ciphers=aes128-cbc admin2@78.90.200.10 << EOF
configure terminal
$(cat /tmp/$NOMBRE_SCRIPT)
end
EOF
