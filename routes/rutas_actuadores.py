from fastapi import APIRouter

router = APIRouter(tags=["Actuadores"])

# Estado en memoria (simple, sin DB)
estado_actuadores = {
    "extractor": False,
    "foco": False,
    "actualizado": 0  # timestamp del último cambio
}

import time

# La página web llama esto para dar una orden
@router.post("/actuadores/comando")
def set_comando(extractor: bool, foco: bool):
    estado_actuadores["extractor"] = extractor
    estado_actuadores["foco"] = foco
    estado_actuadores["actualizado"] = time.time()
    return {"ok": True}

# El ESP32 llama esto cada 5 segundos para ver qué hacer
@router.get("/actuadores/estado")
def get_estado():
    return estado_actuadores
