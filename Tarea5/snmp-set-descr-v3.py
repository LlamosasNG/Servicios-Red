# snmp-set-ifAlias-v3.py
# Asigna una descripción a cada interface utilizando SNMP versión 3
# Generado por ChatGPT 2025

from pysnmp.hlapi import *

# Función para asignar la descripción a una interfaz
def asignar_descripcion(ip, index, descripcion):
    oid = ObjectType(
        ObjectIdentity('1.3.6.1.2.1.31.1.1.1.18.' + str(index)),
        OctetString(descripcion)
    )
    usuario = UsmUserData('usuario', authKey='password123', authProtocol=usmHMACSHAAuthProtocol,
                          privKey='password123', privProtocol=usmAesCfb128Protocol)
    contexto = ContextData()
    protocolo = UdpTransportTarget((ip, 161))
    
    resultado = setCmd(SnmpEngine(), usuario, protocolo, contexto, oid)

    for errorIndication, errorStatus, errorIndex, varBinds in resultado:
        if errorIndication or errorStatus:
            print(f"  • ifIndex {index} ERROR:", errorIndication or errorStatus)
        else:
            print(f"  • ifIndex {index} descripción asignada:", varBinds)

# === Configuración ===
routers = {
    'R1': '3.5.100.10',
    'R2': '3.5.100.11'
}

# Índices de interfaces a las que quieres poner descripción
indices_interfaces = [2, 3, 4]  # Ejemplo: cambia para las interfaces que tú quieras

# Aplicar descripciones
for nombre_router, ip in routers.items():
    print(f"\n=== Configurando descripciones en {nombre_router} ({ip}) ===")
    for index in indices_interfaces:
        descripcion = f"Interface-{index} en {nombre_router}"
        asignar_descripcion(ip, index, descripcion)
