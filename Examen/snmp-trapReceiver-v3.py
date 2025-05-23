# python snmp trap receiver
# Versión SNMP 2: Python SNMP trap receive
# Versión SNMP 3: Carlos Pineda G. 2022

from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

snmpEngine = engine.SnmpEngine()
TrapAgentAddress = '' #Trap listerner address (la cadena vacía '' indica localhost)
Port = 162  #trap listerner port

config.addTransport(
    snmpEngine, 
    udp.domainName, 
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port)))

# para SNMP versión 3 utilizamos un usuario con autenticación y encriptado, así mismo, cada router se identifica con un ID de engine.
# el usuario puede ser el mismo en los diferentes routers.
config.addV3User(snmpEngine,'usuario',config.usmHMACSHAAuthProtocol,'password123',config.usmAesCfb128Protocol,'password123',securityEngineId=v2c.OctetString(hexValue='8000000001020304'))
#config.addV3User(snmpEngine,'usuario',config.usmHMACSHAAuthProtocol,'password123',config.usmAesCfb128Protocol,'password123',securityEngineId=v2c.OctetString(hexValue='8000000001020305'))

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


