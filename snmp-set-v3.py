# snmp-set-v3.py
# Modifica el valor de un objeto utilizando SNMP versión 3
# Generado por ChatGPT. Modificado por Carlos Pineda G. 2022

from pysnmp.hlapi import *
  
# OID a leer
oid = ObjectIdentity('1.3.6.1.2.1.31.1.1.1.18.2') # descripción de la interface Gi0/0   

# Credenciales SNMPv3
usuario = UsmUserData('usuario',authKey='password123',authProtocol=usmHMACSHAAuthProtocol,privKey='password123',privProtocol=usmAesCfb128Protocol)
contexto = ContextData()

# Protocolo SNMPv3
ip = '3.5.200.10'
puerto = 161
protocolo = UdpTransportTarget((ip,puerto))

# Imprimir el resultado de la odificación
resultado = setCmd(SnmpEngine(), usuario, protocolo, contexto, ObjectType(oid, OctetString("esta es otra descripcion")))

# Imprimir valor del OID
for errorIndication, errorStatus, errorIndex, varBinds in resultado:
    if not errorIndication and not errorStatus:
        for varBind in varBinds:
            print(varBind)
    else:
        print("Error:",errorStatus)

