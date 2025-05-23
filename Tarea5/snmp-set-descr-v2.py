# snmp-set-descr-v2.py
# Asigna una descripción a cada interface utilizando SNMP versión 2
# Basado en snmp-get-v2.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# Función para asignar descripción a una interfaz
def asignar_descripcion(ip_router, ifIndex, descripcion):
    oid = ObjectIdentity(f'1.3.6.1.2.1.31.1.1.1.18.{ifIndex}')  # ifAlias

    # Comunidad SNMPv2c
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)
    contexto = ContextData()

    # Protocolo SNMP
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Realizar la operación set
    resultado = setCmd(SnmpEngine(), comunidad, protocolo, contexto, ObjectType(oid, OctetString(descripcion)))

    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                print(f"  • {varBind}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Asignar descripciones en routers ===

print("\n=== Configurando descripciones en R1 (3.5.100.10) ===")
asignar_descripcion('3.5.100.10', 2, "Interface R1 Gi0/0")
asignar_descripcion('3.5.100.10', 3, "Interface R1 Gi1/0")
asignar_descripcion('3.5.100.10', 4, "Interface R1 Gi2/0")

print("\n=== Configurando descripciones en R2 (3.5.100.11) ===")
asignar_descripcion('3.5.100.11', 2, "Interface R2 Gi0/0")
asignar_descripcion('3.5.100.11', 3, "Interface R2 Gi1/0")
