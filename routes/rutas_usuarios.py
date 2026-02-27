from fastapi import APIRouter
from database.db import get_connection
from schemas.usuarios import Usuario

router = APIRouter(tags=["Usuarios"])

@router.get("/getusuarios")
def get_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vista_usuarios")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/getusuario")
def get_usuario(user: Usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL vistau({user.id_usuario})")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/insertusuario")
def insert_usuario(user: Usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL insertar_usuario(
            '{user.nombre}',
            '{user.apellido_p}',
            '{user.apellido_m}',
            '{user.correo}',
            '{user.contra}',
            {user.id_rol}
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/updateusuario")
def update_usuario(user: Usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL actualizar_usuario(
            {user.id_usuario},
            '{user.nombre}',
            '{user.apellido_p}',
            '{user.apellido_m}',
            '{user.correo}',
            '{user.contra}',
            {user.id_rol}
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/delusuario")
def delete_usuario(user: Usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL eliminar_usuario({user.id_usuario})")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}
