# snmp-set-v2-2.py
# Modifica el nombre de un router utilizando SNMP versión 2
# Generado por ChatGPT. Modificado por Carlos Pineda G. 2023

from pysnmp.hlapi import * 

# OID a modificar
oid = ObjectIdentity('SNMPv2-MIB','sysName',0)

# Credenciales SNMPv2
comunidad = CommunityData('prueba')

# Protocolo SNMPv2
ip = '3.5.200.10'
puerto = 161
protocolo = UdpTransportTarget((ip,puerto))

# Modificar valor del OID
valor=OctetString('Router1')
resultado = setCmd(SnmpEngine(), comunidad, protocolo, ContextData(), 
                   ObjectType(oid,valor))

# Imprimir el resultado de la modificación
for errorIndication, errorStatus, errorIndex, varBinds in resultado:
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(varBind)
    else:
        print("Error:",errorStatus)