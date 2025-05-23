# snmp-get-upTime-v2.py
# Obtiene sysUpTime.0 (1.3.6.1.2.1.1.3.0) de R1 y R2 mediante SNMP v2
# Basado en snmp-get-v3.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# Función para obtener el tiempo de funcionamiento
def obtener_uptime(ip_router):
    # OID de sysUpTime.0
    oid = ObjectIdentity('1.3.6.1.2.1.1.3.0')

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

# === Obtener uptime de routers ===

print("\n=== Uptime de R1 (3.5.100.10) ===")
obtener_uptime('3.5.100.10')

print("\n=== Uptime de R2 (3.5.100.11) ===")
obtener_uptime('3.5.100.11')
