from fastapi import APIRouter
from database.db import get_connection
from schemas.dispositivos import Dispositivo

router = APIRouter(tags=["Dispositivos"])

@router.get("/getdispositivos")
def get_dispositivos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vista_dispositivos")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/getdispositivo")
def get_dispositivo(d: Dispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL vistad({d.id_dispositivo})")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/insertdispositivo")
def insert_dispositivo(d: Dispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL insertar_dispositivo(
            '{d.identificador_unico}',
            {d.id_tipo},
            {d.id_espacio},
            '{d.nombre_dispositivo}',
            '{d.informacion_extra}',
            {d.activo}
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/updatedispositivo")
def update_dispositivo(d: Dispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL actualizar_dispositivo(
            {d.id_dispositivo},
            '{d.identificador_unico}',
            {d.id_tipo},
            {d.id_espacio},
            '{d.nombre_dispositivo}',
            '{d.informacion_extra}',
            {d.activo}
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/deldispositivo")
def delete_dispositivo(d: Dispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL eliminar_dispositivo({d.id_dispositivo})")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}
