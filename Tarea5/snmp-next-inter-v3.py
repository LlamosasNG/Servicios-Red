# snmp-next-inter-v3.py
# Obtiene la lista de interfaces (IF‑MIB::ifDescr) de R1 y R2 mediante SNMP v3
# Basado en snmp-get-v3.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# --------------------  CONFIGURACIÓN ESPECÍFICA  --------------------

# OID base de la tabla ifDescr: 1.3.6.1.2.1.2.2.1.2
oid_base = ObjectIdentity('1.3.6.1.2.1.2.2.1.2')

# Diccionario de { alias : IP }
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

for alias, ip in routers.items():
    protocolo = UdpTransportTarget((ip, 161), timeout=2, retries=1)

    print('\n=== Interfaces en {0} ({1}) ==='.format(alias, ip))

    # nextCmd recorre secuencialmente la tabla
    walker = nextCmd(
        SnmpEngine(),
        usuario,
        protocolo,
        contexto,
        ObjectType(oid_base),
        lexicographicMode=False  # se detiene al salir del prefijo
    )

    for errorIndication, errorStatus, errorIndex, varBinds in walker:
        if errorIndication:
            print('ERROR: {0}'.format(errorIndication))
            break
        elif errorStatus:
            print('ERROR: {0}'.format(errorStatus.prettyPrint()))
            break
        else:
            # Cada varBinds contiene un solo par (OID, valor)
            oid_ret, valor = varBinds[0]
            # El último sub‑identificador es el índice de la interfaz
            if_index = int(oid_ret.prettyPrint().split('.')[-1])
            print('  [{0}] {1}'.format(if_index, valor))
