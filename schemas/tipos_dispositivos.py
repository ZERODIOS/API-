from pydantic import BaseModel
from typing import Optional

class TipoDispositivo(BaseModel):
    id_tipo: int = 0
    codigo: str
    nombre: str
    esquema_control: Optional[dict] = None