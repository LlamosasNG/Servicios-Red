from pysnmp.hlapi import *

# Función para obtener las direcciones IP
def obtener_ips(ip_router):
    # OID base de ipAdEntAddr
    oid_base = ObjectIdentity('1.3.6.1.2.1.4.20.1.1')

    # Comunidad SNMPv2c
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)
    contexto = ContextData()

    # Protocolo SNMP
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Realizar el recorrido de direcciones IP
    resultado = nextCmd(SnmpEngine(), comunidad, protocolo, contexto, ObjectType(oid_base), lexicographicMode=False)

    # Imprimir direcciones IP
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                oid, valor = varBind
                print(f"  • {valor.prettyPrint()}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Obtener IPs de routers ===

print("\n=== Direcciones IP en R1 (3.5.100.10) ===")
obtener_ips('3.5.100.10')

print("\n=== Direcciones IP en R2 (3.5.100.11) ===")
obtener_ips('3.5.100.11')
