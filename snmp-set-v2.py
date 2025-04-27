# snmp-set-v2.py
# Modifica el valor de un objeto utilizando SNMP versión 2
# Generado por ChatGPT. Modificado por Carlos Pineda G. 2023

from pysnmp.hlapi import *
  
# OID a modificar
oid = ObjectIdentity('1.3.6.1.2.1.31.1.1.1.18.2') # descripción de la interface Gi0/0

# Credenciales SNMPv2
comunidad = CommunityData('prueba')

# Protocolo SNMPv2
ip = '3.5.200.10'
puerto = 161
protocolo = UdpTransportTarget((ip,puerto))

# Modificar valor del OID
resultado = setCmd(SnmpEngine(), comunidad, protocolo, ContextData(), 
                   ObjectType(oid, OctetString("esta es una descripcion")))

# Imprimir resultado de la modificación
for errorIndication, errorStatus, errorIndex, varBinds in resultado:
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(varBind)
    else:
        print("Error:",errorStatus)
