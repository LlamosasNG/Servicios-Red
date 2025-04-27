# snmp-walk-ipaddr-v3-oid.py
# Obtiene la lista de direcciones IP de R1 y R2 mediante SNMP v3
#   • Para IPv4 usa ipAdEntAddr (1.3.6.1.2.1.4.20.1.1)
# Basado en snmp-get-v3.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# --------------------  CONFIGURACIÓN ESPECÍFICA  --------------------

# OID base de la tabla de direcciones IPv4
oid_base = ObjectIdentity('1.3.6.1.2.1.4.20.1.1')   # ipAdEntAddr

# Diccionario de { alias : IP de gestión }
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

    print('\n=== Direcciones IP en {0} ({1}) ==='.format(alias, ip))

    walker = nextCmd(
        SnmpEngine(),
        usuario,
        protocolo,
        contexto,
        ObjectType(oid_base),
        lexicographicMode=False      # detener al salir del prefijo
    )

    for errorIndication, errorStatus, errorIndex, varBinds in walker:
        if errorIndication:
            print('ERROR: {0}'.format(errorIndication))
            break
        elif errorStatus:
            print('ERROR: {0}'.format(errorStatus.prettyPrint()))
            break
        else:
            # Cada varBind contiene (OID, ipAddress)
            _oid_ret, ip_addr = varBinds[0]
            print('  • {0}'.format(ip_addr.prettyPrint()))
