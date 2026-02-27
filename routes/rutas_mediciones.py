from fastapi import APIRouter
from database.db import get_connection
from schemas.mediciones import Medicion
from routes.rutas_bocina import comandos_pendientes, datetime

router = APIRouter(tags=["Mediciones"])

# ========================================
# CONFIGURACIÓN
# ========================================
UMBRAL_RUIDO = 6  # dB
DISPOSITIVO_BOCINA = "ESP32_BOCINA_01"


@router.get("/getmediciones")
def get_mediciones():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vista_mediciones")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/getmedicion")
def get_medicion(med: Medicion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL vistamd({med.id_medicion})")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/insertmedicion")
def insert_medicion(med: Medicion):
    conn = get_connection()
    cursor = conn.cursor()

    # Insertar medición
    cursor.execute(f"""
        CALL insertar_medicion({med.id_espacio}, {med.temperatura}, {med.humedad},
        {med.co2}, {med.particulas}, {med.ruido}, {med.iluminacion})
    """)
    conn.commit()
    
    # ✨ CONTROL AUTOMÁTICO: Obtener últimas 3 mediciones
    cursor.execute("""
        SELECT ruido 
        FROM mediciones 
        ORDER BY id_medicion DESC 
        LIMIT 3
    """)
    ultimas = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Verificar que tengamos 3 mediciones
    if len(ultimas) >= 3:
        # Extraer valores dependiendo del tipo de resultado
        try:
            # Intentar como tupla primero
            niveles = [med[0] for med in ultimas]
        except (KeyError, TypeError):
            # Si falla, es un diccionario
            niveles = [med['ruido'] for med in ultimas]
        
        print(f"📊 Últimas 3 mediciones: {niveles}")
        
        # Inicializar cola si no existe
        if DISPOSITIVO_BOCINA not in comandos_pendientes:
            comandos_pendientes[DISPOSITIVO_BOCINA] = []
        
        # Si TODAS son mayores a 70 → PLAY
        if all(nivel > UMBRAL_RUIDO for nivel in niveles):
            # Verificar si ya hay comando PLAY pendiente
            tiene_play = any(cmd.get("accion") == "PLAY" for cmd in comandos_pendientes[DISPOSITIVO_BOCINA])
            
            if not tiene_play:
                comandos_pendientes[DISPOSITIVO_BOCINA].append({
                    "accion": "PLAY",
                    "timestamp": datetime.now().isoformat()
                })
                print(f"🔴 Todas > {UMBRAL_RUIDO} dB → Comando PLAY agregado")
        
        # Si TODAS son menores o igual a 70 → STOP
        elif all(nivel <= UMBRAL_RUIDO for nivel in niveles):
            # Verificar si ya hay comando STOP pendiente
            tiene_stop = any(cmd.get("accion") == "STOP" for cmd in comandos_pendientes[DISPOSITIVO_BOCINA])
            
            if not tiene_stop:
                comandos_pendientes[DISPOSITIVO_BOCINA].append({
                    "accion": "STOP",
                    "timestamp": datetime.now().isoformat()
                })
                print(f"🟢 Todas ≤ {UMBRAL_RUIDO} dB → Comando STOP agregado")
        
        else:
            print(f"⚪ Niveles mixtos → Sin cambios")
    
    return {"message": "1"}