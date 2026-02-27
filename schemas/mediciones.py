from pydantic import BaseModel
from datetime import datetime

class Medicion(BaseModel):
    id_medicion: int = 0
    id_espacio: int
    temperatura: float = None
    humedad: float = None
    co2: float = None
    particulas: float = None
    ruido: float = None
    iluminacion: float = None
    # fecha_hora se genera sola