from pysnmp.hlapi import *
import time

def get(OID,ip,puerto):
    while True:
        iterador = getCmd(SnmpEngine(),
                          UsmUserData('usuario',authKey='password123',authProtocol=usmHMACSHAAuthProtocol,privKey='password123',privProtocol=usmAesCfb128Protocol),
                          UdpTransportTarget((ip,puerto)),
                          ContextData(),
                          ObjectType(ObjectIdentity(OID)))
        errorIndication, errorStatus, errorIndex, varBinds = next(iterador)
        if not errorIndication and not errorStatus:
            for name,val in varBinds:
                return val
            else:
                print("Error:",errorIndication)


OID_ifSpeed = '1.3.6.1.2.1.2.2.1.5.4'  # ifSpeed interface Gi2/0
OID_ifInOctets = '1.3.6.1.2.1.2.2.1.10.4'  # ifInOctets interface Gi2/0
ip='3.5.200.10'
puerto=161
tiempo = 10

ifSpeed = float(get(OID_ifSpeed,ip,puerto))
print('ifSpeed=',ifSpeed)

ifInOctets_1 = float(get(OID_ifInOctets,ip,puerto))

while True:
    time.sleep(tiempo)
    ifInOctets_2 = float(get(OID_ifInOctets,ip,puerto))
    porcentaje_utilizacion = ((ifInOctets_2-ifInOctets_1)*8*100)/(tiempo*ifSpeed)
    print(porcentaje_utilizacion)
    ifInOctets_1 = ifInOctets_2
