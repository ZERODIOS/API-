from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario: int = 0
    nombre: str
    apellido_p: str
    apellido_m: str
    correo: str
    contra: str
    id_rol: int