from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

router = APIRouter(prefix="/api/bocina", tags=["Control de Bocina"])

# ========================================
# ALMACENAMIENTO EN MEMORIA
# ========================================
comandos_pendientes: Dict[str, List[dict]] = {}
estados_dispositivos: Dict[str, dict] = {}

# ========================================
# MODELOS PYDANTIC
# ========================================
class Comando(BaseModel):
    accion: str  # PLAY, STOP, VOLUMEN
    valor: Optional[int] = None

class EstadoDispositivo(BaseModel):
    dispositivo_id: str
    reproduciendo: bool
    volumen: int
    wifi_signal: int

# ========================================
# ENDPOINTS PARA ESP32 (Cliente)
# ========================================
@router.post("/estado")
async def recibir_estado(estado: EstadoDispositivo):
    """
    ESP32 reporta su estado actual
    Llamado cada 3-5 segundos por el ESP32
    """
    estados_dispositivos[estado.dispositivo_id] = {
        **estado.dict(),
        "timestamp": datetime.now().isoformat(),
        "online": True
    }
    return {"status": "ok", "mensaje": "Estado actualizado"}

@router.get("/comandos")
async def obtener_comandos(dispositivo_id: str):
    """
    ESP32 consulta comandos pendientes
    Retorna lista de comandos y limpia la cola
    """
    if dispositivo_id not in comandos_pendientes:
        return {"comandos": []}
    
    # Obtener comandos y limpiar cola
    comandos = comandos_pendientes[dispositivo_id]
    comandos_pendientes[dispositivo_id] = []
    
    return {
        "comandos": comandos,
        "total": len(comandos)
    }

# ========================================
# ENDPOINTS PARA INTERFAZ WEB (Control)
# ========================================
@router.post("/play")
async def sonido_play(dispositivo_id: str = "ESP32_BOCINA_01"):
    """▶️ Reproducir ruido blanco"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    # Agregar comando a la cola
    comandos_pendientes[dispositivo_id].append({
        "accion": "PLAY",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "PLAY",
        "dispositivo": dispositivo_id
    }

@router.post("/stop")
async def sonido_stop(dispositivo_id: str = "ESP32_BOCINA_01"):
    """⏹️ Detener ruido blanco"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "STOP",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "STOP",
        "dispositivo": dispositivo_id
    }

@router.post("/volumen")
async def sonido_volumen(valor: int, dispositivo_id: str = "ESP32_BOCINA_01"):
    """🔊 Cambiar volumen (0-100)"""
    if not 0 <= valor <= 100:
        raise HTTPException(status_code=400, detail="Volumen debe estar entre 0 y 100")
    
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "VOLUMEN",
        "valor": valor,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "VOLUMEN",
        "volumen": valor,
        "dispositivo": dispositivo_id
    }

@router.get("/status")
async def sonido_status(dispositivo_id: str = "ESP32_BOCINA_01"):
    """📊 Obtener último estado reportado por el dispositivo"""
    if dispositivo_id not in estados_dispositivos:
        raise HTTPException(
            status_code=404, 
            detail=f"Dispositivo '{dispositivo_id}' no encontrado o nunca se ha conectado"
        )
    
    estado = estados_dispositivos[dispositivo_id]
    
    # Verificar si el dispositivo sigue online (última actualización < 15 segundos)
    ultima_actualizacion = datetime.fromisoformat(estado["timestamp"])
    diferencia = (datetime.now() - ultima_actualizacion).total_seconds()
    estado["online"] = diferencia < 15
    
    return estado

@router.get("/dispositivos")
async def listar_dispositivos():
    """📱 Listar todos los dispositivos conectados"""
    return {
        "dispositivos": list(estados_dispositivos.keys()),
        "total": len(estados_dispositivos),
        "estados": estados_dispositivos
    }

@router.delete("/comandos/{dispositivo_id}")
async def limpiar_comandos(dispositivo_id: str):
    """🗑️ Limpiar cola de comandos pendientes"""
    if dispositivo_id in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
        return {"status": "ok", "mensaje": "Cola limpiada"}
    return {"status": "ok", "mensaje": "No había comandos pendientes"}