# snmp-bulk-v2.py
# Obtiene una tabla utilizando SNMP versión 2
# Generado por ChatGPT. Modificado por Carlos Pineda G. 2023

from pysnmp.hlapi import *
  
# OID a leer
oid = ObjectIdentity('1.3.6.1.2.1.2.2.1.2'); # interfaces

# Comunidad SNMP
cadena_comunidad = "prueba"
comunidad = CommunityData(cadena_comunidad, mpModel=1)

# Protocolo SNMP
ip = '3.5.200.10'
puerto = 161
protocolo = UdpTransportTarget((ip,puerto))

# Leer valor del OID no escalar
resultado = bulkCmd(SnmpEngine(), comunidad, protocolo, ContextData(), 0, 2, 
                    ObjectType(oid),lexicographicMode=False)

# Imprimir valor del OID
for errorIndication, errorStatus, errorIndex, varBinds in resultado:
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(varBind)
    else:
        print("Error:",errorStatus)