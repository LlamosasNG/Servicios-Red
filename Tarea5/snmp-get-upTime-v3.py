# snmp-get-upTime-v3.py
# Obtiene sysUpTime.0 (1.3.6.1.2.1.1.3.0) de R1 y R2 mediante SNMP v3
# Basado en snmp-get-v3.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# --------------------  CONFIGURACIÓN ESPECÍFICA  --------------------

# OID numérico del tiempo de funcionamiento (sysUpTime.0)
oid = ObjectIdentity('1.3.6.1.2.1.1.3.0')

# Lista de routers destino { alias : IP }
routers = {
    'R1': '3.5.100.10',
    'R2': '3.5.100.11',
}

# Credenciales SNMPv3 (authPriv)
usuario = UsmUserData(
    'usuario',
    authKey='password123',
    authProtocol=usmHMACSHAAuthProtocol,
    privKey='password123',
    privProtocol=usmAesCfb128Protocol
)

# Contexto SNMP (vacío normalmente)
contexto = ContextData()

# -------------------------------------------------------------------

print('=== sysUpTime vía SNMP v3 (authPriv) ===')
for nombre, ip in routers.items():
    # Transporte SNMP
    protocolo = UdpTransportTarget((ip, 161), timeout=2, retries=1)

    # Petición GET
    resultado = getCmd(
        SnmpEngine(),
        usuario,
        protocolo,
        contexto,
        ObjectType(oid)
    )

    # Procesar respuesta
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            # Solo hay un varBind (sysUpTime.0)
            oid_ret, valor = varBinds[0]
            print('{0} ({1}) → {2}'.format(nombre, ip, valor))
        else:
            print('{0} ({1}) → ERROR: {2}'.format(
                nombre,
                ip,
                errorIndication or errorStatus.prettyPrint()
            ))
