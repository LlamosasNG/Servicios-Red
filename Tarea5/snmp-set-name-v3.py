# snmp-set-sysname-v3-oid.py
# Cambia sysName.0 en R1 y R2 mediante SNMP v3 (authPriv)
#   R1 → “Router1”
#   R2 → “Router2”
# Basado en snmp-get-v3.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# --------------------  CONFIGURACIÓN ESPECÍFICA  --------------------

# OID numérico del nombre del host (sysName.0)
oid = ObjectIdentity('1.3.6.1.2.1.1.5.0')

# Diccionario de { alias : (IP , nuevo_nombre) }
routers = {
    'R1': ('3.5.100.10',  'Router1'),
    'R2': ('3.5.100.11', 'Router2'),
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

print('=== Cambio de sysName vía SNMP v3 (authPriv) ===')
for alias, (ip, nuevo_nombre) in routers.items():
    protocolo = UdpTransportTarget((ip, 161), timeout=2, retries=1)

    # Petición SET
    resultado = setCmd(
        SnmpEngine(),
        usuario,
        protocolo,
        contexto,
        ObjectType(oid, OctetString(nuevo_nombre))
    )

    # Procesar respuesta
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            print('{0} ({1}) → Nombre cambiado a “{2}”'.format(alias, ip, nuevo_nombre))
        else:
            print('{0} ({1}) → ERROR: {2}'.format(
                alias,
                ip,
                errorIndication or errorStatus.prettyPrint()
            ))
