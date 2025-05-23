# snmp-next-inter-v2.py
# Obtiene la lista de interfaces (IF‑MIB::ifDescr) de R1 y R2 mediante SNMP v2
# Basado en snmp-get-v2.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# Función para obtener las interfaces
def obtener_interfaces(ip_router):
    # OID base de ifDescr
    oid_base = ObjectIdentity('1.3.6.1.2.1.2.2.1.2')

    # Comunidad SNMPv2c
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)
    contexto = ContextData()

    # Protocolo SNMP
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Realizar el recorrido de interfaces
    resultado = nextCmd(SnmpEngine(), comunidad, protocolo, contexto, ObjectType(oid_base), lexicographicMode=False)

    # Imprimir interfaces
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                oid, valor = varBind
                indice = oid.prettyPrint().split('.')[-1]
                print(f"  [{indice}] {valor.prettyPrint()}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Obtener interfaces de routers ===

print("\n=== Interfaces en R1 (3.5.100.10) ===")
obtener_interfaces('3.5.100.10')

print("\n=== Interfaces en R2 (3.5.100.11) ===")
obtener_interfaces('3.5.100.11')
