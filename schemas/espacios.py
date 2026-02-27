from pydantic import BaseModel

class Espacio(BaseModel):
    id_espacio: int = 0
    nombre: str
    planta: str
    capacidad: int
    id_usuario: int