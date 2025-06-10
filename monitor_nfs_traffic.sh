#!/bin/bash

# Script de monitoreo NFS - Extracción corregida
# Autor: Gonzalez Llamosas Noe Ramses
# Fecha: 2025-06-09

ROUTER_IP="3.5.200.10"
ROUTER_USER="admin"
ROUTER_PASS="123456"
OUTPUT_FILE="salida.csv"
DEBUG_FILE="debug.log"
COUNTER=1
PREV_BYTES=0

# Parámetros SSH que funcionan
SSH_OPTS="-o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o Ciphers=aes128-cbc"

# Función de limpieza
cleanup() {
    echo "Deteniendo monitoreo..."
    exit 0
}
trap cleanup SIGINT

# Función corregida para extraer SOLO los bytes de NFS-TRAFFIC
extract_nfs_bytes() {
    local output="$1"
    local bytes=""
    
    echo "=== ANÁLISIS DE EXTRACCIÓN DE BYTES ===" >> "$DEBUG_FILE"
    echo "Salida completa a analizar:" >> "$DEBUG_FILE"
    echo "$output" >> "$DEBUG_FILE"
    echo "==============================" >> "$DEBUG_FILE"
    
    # Método 1: Extraer específicamente de la línea de NFS-TRAFFIC
    # Buscar la línea que contiene "Class-map: NFS-TRAFFIC" y luego la siguiente línea con packets y bytes
    bytes=$(echo "$output" | awk '
        /Class-map: NFS-TRAFFIC/ { 
            getline; 
            if ($0 ~ /packets.*bytes/) {
                # Extraer el número antes de "bytes"
                match($0, /([0-9]+) bytes/, arr)
                if (arr[1]) print arr[1]
            }
        }')
    
    echo "Método 1 (awk específico): '$bytes'" >> "$DEBUG_FILE"
    
    # Método 2: Si el método 1 falla, usar sed más específico
    if [[ -z "$bytes" ]]; then
        bytes=$(echo "$output" | sed -n '/Class-map: NFS-TRAFFIC/,/Class-map:/p' | \
                grep -E '[0-9]+ packets, [0-9]+ bytes' | \
                sed 's/.* \([0-9]\+\) bytes.*/\1/' | head -1)
        echo "Método 2 (sed específico): '$bytes'" >> "$DEBUG_FILE"
    fi
    
    # Método 3: Buscar directamente después de "NFS-TRAFFIC"
    if [[ -z "$bytes" ]]; then
        bytes=$(echo "$output" | grep -A 3 "NFS-TRAFFIC" | \
                grep -E 'packets.*bytes' | head -1 | \
                grep -oE '[0-9]+ bytes' | grep -oE '[0-9]+')
        echo "Método 3 (grep -A): '$bytes'" >> "$DEBUG_FILE"
    fi
    
    # Limpiar y validar el número
    bytes=$(echo "$bytes" | tr -d '\n\r\t ' | head -1)
    
    # Si no es un número válido, usar 0
    if [[ ! "$bytes" =~ ^[0-9]+$ ]]; then
        echo "Número no válido encontrado: '$bytes', usando 0" >> "$DEBUG_FILE"
        bytes="0"
    fi
    
    echo "Bytes finales extraídos: '$bytes'" >> "$DEBUG_FILE"
    echo "$bytes"
}

# Función para obtener salida del router
get_router_output() {
    local full_output
    full_output=$(timeout 15 sshpass -p "$ROUTER_PASS" ssh $SSH_OPTS \
        "${ROUTER_USER}@${ROUTER_IP}" \
        "show policy-map interface gi2/0" 2>&1)
    
    local ssh_exit_code=$?
    
    if [[ $ssh_exit_code -ne 0 ]]; then
        echo "Error SSH (código: $ssh_exit_code): $full_output" | tee -a "$DEBUG_FILE"
        return 1
    fi
    
    echo "$full_output"
    return 0
}

# Verificar dependencias
if ! command -v sshpass &> /dev/null; then
    echo "Error: sshpass no está instalado"
    exit 1
fi

# Inicializar archivos
echo "Iniciando monitoreo de tráfico NFS..." | tee "$DEBUG_FILE"
echo "Fecha: $(date)" | tee -a "$DEBUG_FILE"
echo "========================================" | tee -a "$DEBUG_FILE"

> "$OUTPUT_FILE"  # Limpiar archivo CSV

echo "Presiona Ctrl+C para detener"
echo "Monitoreando tráfico NFS específicamente..."

# Bucle principal
while true; do
    echo "--- Iteración $COUNTER ($(date)) ---" >> "$DEBUG_FILE"
    
    # Obtener salida del router
    router_output=$(get_router_output)
    connection_status=$?
    
    if [[ $connection_status -eq 0 ]]; then
        # Extraer bytes específicos de NFS-TRAFFIC
        current_bytes=$(extract_nfs_bytes "$router_output")
        
        # Validar número
        if [[ ! "$current_bytes" =~ ^[0-9]+$ ]]; then
            current_bytes=0
        fi
        
        # Calcular BPS
        if [[ $COUNTER -gt 1 ]]; then
            byte_diff=$((current_bytes - PREV_BYTES))
            
            # Si la diferencia es negativa (contador reiniciado), usar bytes actuales
            if [[ $byte_diff -lt 0 ]]; then
                byte_diff=$current_bytes
            fi
            
            bps=$((byte_diff * 8))
        else
            bps=0
            byte_diff=0
        fi
        
        # Guardar resultado
        echo "${COUNTER},${bps}" >> "$OUTPUT_FILE"
        
        # Mostrar información detallada
        echo "✓ Tiempo: ${COUNTER}s, Bytes NFS: ${current_bytes}, Diferencia: ${byte_diff}, BPS: ${bps}"
        
        PREV_BYTES=$current_bytes
        
    else
        # Error de conexión
        echo "${COUNTER},0" >> "$OUTPUT_FILE"
        echo "✗ Tiempo: ${COUNTER}s, Error de conexión, BPS: 0"
    fi
    
    ((COUNTER++))
    sleep 1
done