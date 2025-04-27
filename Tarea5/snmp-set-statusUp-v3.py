# snmp-set-ifAdminStatus-v3.py
# Enciende interfaces específicas utilizando SNMP versión 3
# Generado por ChatGPT 2025
from pysnmp.hlapi import *

# Función para encender una interfaz
def encender_interface(ip_router, ifIndex):
    # OID para ifAdminStatus de la interfaz específica
    oid = ObjectIdentity('1.3.6.1.2.1.2.2.1.7.' + str(ifIndex))  # ifAdminStatus.{ifIndex}

    # Credenciales SNMPv3
    usuario = UsmUserData('usuario', authKey='password123', authProtocol=usmHMACSHAAuthProtocol,
                          privKey='password123', privProtocol=usmAesCfb128Protocol)
    contexto = ContextData()

    # Protocolo SNMPv3
    puerto = 161
    protocolo = UdpTransportTarget((ip_router, puerto))

    # Realizar el setCmd para encender la interfaz (valor 1 = up)
    resultado = setCmd(SnmpEngine(), usuario, protocolo, contexto, ObjectType(oid, Integer(1)))

    # Imprimir resultado
    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if not errorIndication and not errorStatus:
            for varBind in varBinds:
                print(f"  • {varBind}")
        else:
            print(f"  • ERROR: {errorStatus.prettyPrint()}")

# === Encender interfaces ===

print("\n=== Encendiendo interfaces ===")
print("En R1 (3.5.100.10) - Gi2/0")
encender_interface('3.5.100.10', 4)  # Recuerda: Gi2/0 corresponde a ifIndex 4

print("\nEn R2 (3.5.100.11) - Gi1/0")
encender_interface('3.5.100.11', 3)  # Gi1/0 corresponde a ifIndex 3