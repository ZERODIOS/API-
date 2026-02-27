from pydantic import BaseModel

class Rol(BaseModel):
    id_rol: int = 0
    rol: int