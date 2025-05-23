# snmp-set-statusDown-v2.py
# Apaga interfaces específicas utilizando SNMP versión 2
# Basado en snmp-get-v2.py. Modificado por ChatGPT ─ 2025

from pysnmp.hlapi import *

# Función para apagar una interfaz
def apagar_interface(ip_router, ifIndex):
    oid = ObjectIdentity(f'1.3.6.1.2.1.2.2.1.7.{ifIndex}')  # ifAdminStatus

    # Comunidad SNMPv2c
    cadena_comunidad = "prueba"
    comunidad = CommunityData(cadena_comunidad, mpModel=1)
    contexto = ContextData()

    # Protocolo SNMP
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Realizar la operación set
    resultado = setCmd(SnmpEngine(), comunidad, protocolo, contexto, ObjectType(oid, Integer(2)))  # 2 = down

    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                print(f"  • {varBind}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Apagar interfaces en routers ===

print("\n=== Apagando interfaces en R1 (3.5.100.10) ===")
apagar_interface('3.5.100.10', 4)  # Gi2/0 en R1

print("\n=== Apagando interfaces en R2 (3.5.100.11) ===")
apagar_interface('3.5.100.11', 3)  # Gi1/0 en R2
