from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Control de Dispositivos"])

# ========================================
# ALMACENAMIENTO EN MEMORIA
# ========================================
comandos_pendientes: Dict[str, List[dict]] = {}
estados_dispositivos: Dict[str, dict] = {}

# ========================================
# MODELOS PYDANTIC
# ========================================
class EstadoDispositivo(BaseModel):
    dispositivo_id: str
    ventilador_encendido: bool
    foco_encendido: bool
    foco_intensidad: int  # 0-100 o 100-1000 según Tuya
    modo_automatico: bool
    temperatura: Optional[float] = None
    humedad: Optional[float] = None
    pm25: Optional[int] = None
    lux: Optional[float] = None

# ========================================
# 🌀 ENDPOINTS VENTILADOR
# ========================================
@router.post("/ventilador/on")
async def ventilador_on(dispositivo_id: str = "ESP32_AURA_01"):
    """🌀 Encender ventilador (modo manual)"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "VENTILADOR_ON",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "VENTILADOR_ON",
        "dispositivo": dispositivo_id
    }

@router.post("/ventilador/off")
async def ventilador_off(dispositivo_id: str = "ESP32_AURA_01"):
    """🌀 Apagar ventilador (modo manual)"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "VENTILADOR_OFF",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "VENTILADOR_OFF",
        "dispositivo": dispositivo_id
    }

# ========================================
# 💡 ENDPOINTS FOCO
# ========================================
@router.post("/foco/on")
async def foco_on(dispositivo_id: str = "ESP32_AURA_01"):
    """💡 Encender foco (modo manual)"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "FOCO_ON",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "FOCO_ON",
        "dispositivo": dispositivo_id
    }

@router.post("/foco/off")
async def foco_off(dispositivo_id: str = "ESP32_AURA_01"):
    """💡 Apagar foco (modo manual)"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "FOCO_OFF",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "FOCO_OFF",
        "dispositivo": dispositivo_id
    }

@router.post("/foco/intensidad")
async def foco_intensidad(intensidad: int, dispositivo_id: str = "ESP32_AURA_01"):
    """💡 Cambiar intensidad del foco (0-100)"""
    if not 0 <= intensidad <= 100:
        raise HTTPException(status_code=400, detail="Intensidad debe estar entre 0 y 100")
    
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    # Convertir de 0-100 a 100-1000 para Tuya
    brillo_tuya = int((intensidad / 100) * 900 + 100)
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "FOCO_INTENSIDAD",
        "valor": intensidad,
        "brillo_tuya": brillo_tuya,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "accion": "FOCO_INTENSIDAD",
        "intensidad": intensidad,
        "brillo_tuya": brillo_tuya,
        "dispositivo": dispositivo_id
    }

# ========================================
# 🔄 MODO DE OPERACIÓN
# ========================================
@router.post("/modo")
async def cambiar_modo(automatico: bool, dispositivo_id: str = "ESP32_AURA_01"):
    """🔄 Cambiar entre modo manual y automático"""
    if dispositivo_id not in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
    
    comandos_pendientes[dispositivo_id].append({
        "accion": "MODO_AUTOMATICO" if automatico else "MODO_MANUAL",
        "valor": automatico,
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "status": "comando_enviado",
        "modo": "automatico" if automatico else "manual",
        "dispositivo": dispositivo_id
    }

# ========================================
# 📊 ENDPOINTS PARA ESP32 (Cliente)
# ========================================
@router.post("/estado")
async def recibir_estado(estado: EstadoDispositivo):
    """ESP32 reporta su estado actual"""
    estados_dispositivos[estado.dispositivo_id] = {
        **estado.dict(),
        "timestamp": datetime.now().isoformat(),
        "online": True
    }
    return {"status": "ok", "mensaje": "Estado actualizado"}

@router.get("/comandos")
async def obtener_comandos(dispositivo_id: str):
    """ESP32 consulta comandos pendientes"""
    if dispositivo_id not in comandos_pendientes:
        return {"comandos": []}
    
    comandos = comandos_pendientes[dispositivo_id]
    comandos_pendientes[dispositivo_id] = []
    
    return {
        "comandos": comandos,
        "total": len(comandos)
    }

@router.get("/status")
async def obtener_status(dispositivo_id: str = "ESP32_AURA_01"):
    """📊 Obtener último estado reportado"""
    if dispositivo_id not in estados_dispositivos:
        raise HTTPException(
            status_code=404, 
            detail=f"Dispositivo '{dispositivo_id}' no encontrado"
        )
    
    estado = estados_dispositivos[dispositivo_id]
    
    # Verificar si está online (última actualización < 15 seg)
    ultima_actualizacion = datetime.fromisoformat(estado["timestamp"])
    diferencia = (datetime.now() - ultima_actualizacion).total_seconds()
    estado["online"] = diferencia < 15
    
    return estado

@router.get("/dispositivos")
async def listar_dispositivos():
    """📱 Listar todos los dispositivos"""
    return {
        "dispositivos": list(estados_dispositivos.keys()),
        "total": len(estados_dispositivos),
        "estados": estados_dispositivos
    }

@router.delete("/comandos/{dispositivo_id}")
async def limpiar_comandos(dispositivo_id: str):
    """🗑️ Limpiar cola de comandos"""
    if dispositivo_id in comandos_pendientes:
        comandos_pendientes[dispositivo_id] = []
        return {"status": "ok", "mensaje": "Cola limpiada"}
    return {"status": "ok", "mensaje": "No había comandos pendientes"}