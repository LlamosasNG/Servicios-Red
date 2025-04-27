# snmp-next-v2-2.py
# Obtiene la lista de interfaces de un rouiter utilizando SNMP versión 2
# Generado por ChatGPT. Modificado por Carlos Pineda G. 2023

from pysnmp.hlapi import * 

# OID a leer
oid = ObjectIdentity('IF-MIB','ifDescr')

# Comunidad SNMP
cadena_comunidad = "prueba"
comunidad = CommunityData(cadena_comunidad, mpModel=1)

# Protocolo SNMP
ip = '3.5.200.10'
puerto = 161
protocolo = UdpTransportTarget((ip,puerto))

# Leer valor del OID no escalar
resultado = nextCmd(SnmpEngine(), comunidad, protocolo, ContextData(),
                    ObjectType(oid),lexicographicMode=False)

# Imprimir valor del OID
for errorIndication, errorStatus, errorIndex, varBinds in resultado:
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(varBind)
    else:
        print("Error:",errorStatus)
