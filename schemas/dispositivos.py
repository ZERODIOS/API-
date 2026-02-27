from pydantic import BaseModel
from typing import Optional

class Dispositivo(BaseModel):
    id_dispositivo: int = 0
    identificador_unico: str
    id_tipo: int
    id_espacio: Optional[int] = None
    nombre_dispositivo: str
    informacion_extra: Optional[dict] = None
    activo: int = 1