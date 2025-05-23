# snmp-set-name-v2.py
# Cambia sysName.0 en R1 y R2 mediante SNMP v2
#   R1 → “R1”
#   R2 → “R2”
# Basado en snmp-get-v2.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# Función para cambiar el nombre del router
def cambiar_nombre(ip_router, nuevo_nombre):
    # OID de sysName.0
    oid = ObjectIdentity('1.3.6.1.2.1.1.5.0')

    # Comunidad SNMPv2c
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)
    contexto = ContextData()

    # Protocolo SNMP
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Realizar la modificación
    resultado = setCmd(SnmpEngine(), comunidad, protocolo, contexto, ObjectType(oid, OctetString(nuevo_nombre)))

    # Imprimir resultado
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                print(f"  • {varBind}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Cambiar nombres de routers ===

print("\n=== Cambiando nombre de R1 (3.5.100.10) ===")
cambiar_nombre('3.5.100.10', 'R1')

print("\n=== Cambiando nombre de R2 (3.5.100.11) ===")
cambiar_nombre('3.5.100.11', 'R2')
