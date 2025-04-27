# snmp-trapReceiver-v2.py
# python snmp trap receiver
# Fuente: Python SNMP trap receive
# Modificado por Carlos Pineda G. 2022

from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

snmpEngine = engine.SnmpEngine()
TrapAgentAddress = '' # Trap listerner address (la cadena vacía '' indica localhost)
Port = 162 # trap listerner port

config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port)))

# para SNMP versión 2 se utiliza una cadena de comunidad y un ID de engine para cada router.
# la cadena de comunidad y el ID de engine deben ser diferentes en cada router.
config.addV1System(snmpEngine,'nombre_1','prueba_1',v2c.OctetString(hexValue='8000000001020304'))
config.addV1System(snmpEngine,'nombre_2','prueba_2',v2c.OctetString(hexValue='8000000001020305'))

# esta función es invocada cada vez que se recibe una notificación
def cbFun(snmpEngine,stateReference,contextEngineId,contextName,varBinds,cbCtx):
    print("Received new Trap message")
    print("contextEngineId=",contextEngineId.prettyPrint())
    for name, val in varBinds:
        print(name,'=',val)

# define la función que será invocada cuando se reciba una notificación
ntfrcv.NotificationReceiver(snmpEngine,cbFun)
snmpEngine.transportDispatcher.jobStarted(1)
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise

