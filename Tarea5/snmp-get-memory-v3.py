# snmp-get-freemem-v3-oid.py
# Obtiene la memoria libre (bytes) en el Pool “Processor” de R1 y R2 por SNMP v3
# Basado en snmp-get-v3.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# --------------------  CONFIGURACIÓN ESPECÍFICA  --------------------
#
# En equipos Cisco, la memoria libre por “Memory Pool” se encuentra en la MIB:
#   CISCO‑MEMORY‑POOL‑MIB::ciscoMemoryPoolFree
# El OID numérico es 1.3.6.1.4.1.9.9.48.1.1.1.6.<index>
# Habitualmente, el índice 1 corresponde al pool “Processor”.
# Si tu router muestra otro índice, cámbialo abajo.

POOL_INDEX = 1
oid = ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1.6.{0}'.format(POOL_INDEX))

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

print('=== Memoria libre (Processor Pool) vía SNMP v3 (authPriv) ===')
for nombre, ip in routers.items():
    protocolo = UdpTransportTarget((ip, 161), timeout=2, retries=1)

    resultado = getCmd(
        SnmpEngine(),
        usuario,
        protocolo,
        contexto,
        ObjectType(oid)
    )

    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            _, valor = varBinds[0]   # valor en bytes
            # Convertir a MiB para hacerlo más legible
            mib = int(valor) / (1024 * 1024.0)
            print('{0} ({1}) → {2:.2f} MiB libres'.format(nombre, ip, mib))
        else:
            print('{0} ({1}) → ERROR: {2}'.format(
                nombre,
                ip,
                errorIndication or errorStatus.prettyPrint()
            ))

