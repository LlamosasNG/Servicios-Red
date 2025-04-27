snmpget -v3 -l authPriv -u usuario -a SHA -A password123 -x AES -X password123 3.5.50.1 1.3.6.1.2.1.1.1.0
snmpget -v2c -c prueba 3.5.50.1 1.3.6.1.2.1.1.1.0
snmpwalk -v3 -l authPriv -u usuario -a SHA -A password123 -x AES -X password123 3.5.50.1
