# snmp-get-v2.py
# Obtiene un objeto utilizando SNMP versión 2
# Generado por ChatGPT. Modificado por Carlos Pineda G. 2023

from pysnmp.hlapi import *

# OID a leer
oid = ObjectIdentity('1.3.6.1.2.1.1.5.0') # nombre del host

# Comunidad SNMP
cadena_comunidad = "prueba"
comunidad = CommunityData(cadena_comunidad, mpModel=1)

# Protocolo SNMP
ip = '3.5.200.10'
puerto = 161
protocolo = UdpTransportTarget((ip,puerto))

# Obtener valor del OID
resultado = getCmd(SnmpEngine(), comunidad, protocolo, ContextData(), ObjectType(oid))

# Imprimir valor del OID
for errorIndication, errorStatus, errorIndex, varBinds in resultado:
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(varBind)
    else:
        print("Error:",errorStatus)
