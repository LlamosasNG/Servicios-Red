from pysnmp.hlapi import *

# Función para obtener el nombre de un router
def obtener_nombre_router(ip_router):
    # OID de sysName.0
    oid = ObjectIdentity('1.3.6.1.2.1.1.5.0')

    # Comunidad SNMP
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)

    # Protocolo SNMPv2c
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Obtener valor del OID
    resultado = getCmd(SnmpEngine(), comunidad, protocolo, ContextData(), ObjectType(oid))

    # Imprimir resultado
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                print(f"  • {varBind}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Obtener nombre de routers ===

print("\n=== Nombre de R1 (3.5.100.10) ===")
obtener_nombre_router('3.5.100.10')

print("\n=== Nombre de R2 (3.5.100.11) ===")
obtener_nombre_router('3.5.100.11')
