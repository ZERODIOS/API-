from fastapi import APIRouter
from database.db import get_connection
from schemas.roles import Rol

router = APIRouter(tags=["Roles"])

@router.get("/getroles")
def get_roles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vista_roles")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/getrol")
def get_rol(rol: Rol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL vistarol({rol.id_rol})")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/insertrol")
def insert_rol(rol: Rol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL insertar_rol('{rol.rol}')")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/updaterol")
def update_rol(rol: Rol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL actualizar_rol({rol.id_rol}, '{rol.rol}')")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/delrol")
def delete_rol(rol: Rol):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL eliminar_rol({rol.id_rol})")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}
