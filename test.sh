
ROUTER_IP="3.5.200.10"
ROUTER_USER="admin"
ROUTER_PASS="123456"
SSH_OPTS="-o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o Ciphers=aes128-cbc"

echo "=== DEBUG DETALLADO DE EXTRACCIÓN NFS ==="

# Obtener salida del router
router_output=$(sshpass -p "$ROUTER_PASS" ssh $SSH_OPTS \
    "${ROUTER_USER}@${ROUTER_IP}" \
    "show policy-map interface gi2/0" 2>&1)

echo "1. SALIDA COMPLETA DEL ROUTER:"
echo "=============================="
echo "$router_output"
echo "=============================="

echo -e "\n2. LÍNEAS QUE CONTIENEN 'NFS-TRAFFIC':"
echo "$router_output" | grep -n "NFS-TRAFFIC"

echo -e "\n3. SECCIÓN COMPLETA DE NFS-TRAFFIC:"
echo "$router_output" | sed -n '/Class-map: NFS-TRAFFIC/,/Class-map:/p' | head -10

echo -e "\n4. LÍNEAS CON 'packets' y 'bytes':"
echo "$router_output" | grep -E 'packets.*bytes'

echo -e "\n5. EXTRACCIÓN MÉTODO AWK:"
nfs_bytes=$(echo "$router_output" | awk '
    /Class-map: NFS-TRAFFIC/ { 
        getline; 
        if ($0 ~ /packets.*bytes/) {
            match($0, /([0-9]+) bytes/, arr)
            if (arr[1]) print arr[1]
        }
    }')
echo "Bytes extraídos: '$nfs_bytes'"

echo -e "\n6. VERIFICACIÓN MANUAL:"
echo "Según tu salida, debería extraer: 74622"
echo "¿Coincide? $(if [[ "$nfs_bytes" == "74622" ]]; then echo "SÍ"; else echo "NO - Encontrado: $nfs_bytes"; fi)"