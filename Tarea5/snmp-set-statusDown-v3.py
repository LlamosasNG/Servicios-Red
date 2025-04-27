# snmp-set-ifAdminStatus-v3.py
# Apaga interfaces específicas utilizando SNMP versión 3
# Generado por ChatGPT 2025

from pysnmp.hlapi import *

# Función para apagar una interfaz
def apagar_interface(ip, index):
    oid = ObjectType(
        ObjectIdentity('1.3.6.1.2.1.2.2.1.7.' + str(index)),
        Integer(2)  # 2 = down
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
            print(f"  • ifIndex {index} apagada correctamente")

# === Configuración ===
# Específicamente los índices que quieres apagar
# Recuerda: debes conocer el ifIndex correcto de Gi2/0 y Gi1/0

routers = {
    'R1': {'ip': '3.5.100.10', 'index': 4},  # Gi2/0 → ifIndex 4
    'R2': {'ip': '3.5.100.11', 'index': 3}   # Gi1/0 → ifIndex 3
}

# Apagar las interfaces
for nombre_router, datos in routers.items():
    print(f"\n=== Apagando interfaz en {nombre_router} ({datos['ip']}) ===")
    apagar_interface(datos['ip'], datos['index'])
