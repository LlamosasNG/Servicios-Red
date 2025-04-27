from pysnmp.hlapi import *

# Función para obtener la memoria libre
def obtener_memoria_libre(ip_router):
    # OID de ciscoMemoryPoolFree.1
    oid = ObjectIdentity('1.3.6.1.4.1.9.9.48.1.1.1.6.1')

    # Comunidad SNMPv2c
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)
    contexto = ContextData()

    # Protocolo SNMP
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Obtener valor del OID
    resultado = getCmd(SnmpEngine(), comunidad, protocolo, contexto, ObjectType(oid))

    # Imprimir resultado
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                print(f"  • {varBind}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Obtener memoria libre de routers ===

print("\n=== Memoria libre en R1 (3.5.100.10) ===")
obtener_memoria_libre('3.5.100.10')

print("\n=== Memoria libre en R2 (3.5.100.11) ===")
obtener_memoria_libre('3.5.100.11')
