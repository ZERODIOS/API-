from fastapi import APIRouter
from database.db import get_connection
from schemas.espacios import Espacio

router = APIRouter(tags=["Espacios"])

@router.get("/getespacios")
def get_espacios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vista_espacios")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/getespacio")
def get_espacio(esp: Espacio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL vistae({esp.id_espacio})")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/insertespacio")
def insert_espacio(esp: Espacio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL insertar_espacio(
            '{esp.nombre}',
            '{esp.planta}',
            {esp.capacidad},
            {esp.id_usuario}
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/updateespacio")
def update_espacio(esp: Espacio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL actualizar_espacio(
            {esp.id_espacio},
            '{esp.nombre}',
            '{esp.planta}',
            {esp.capacidad},
            {esp.id_usuario}
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/delespacio")
def delete_espacio(esp: Espacio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL eliminar_espacio({esp.id_espacio})")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}
