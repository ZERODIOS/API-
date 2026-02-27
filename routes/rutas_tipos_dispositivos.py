from fastapi import APIRouter
from database.db import get_connection
from schemas.tipos_dispositivos import TipoDispositivo

router = APIRouter(tags=["Tipos de Dispositivos"])

@router.get("/gettiposdispositivos")
def get_tipos_dispositivos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vista_tipos_dispositivos")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/gettipodispositivo")
def get_tipo_dispositivo(td: TipoDispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL vistatd({td.id_tipo})")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultado


@router.post("/inserttipodispositivo")
def insert_tipo_dispositivo(td: TipoDispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL insertar_tipo_dispositivo(
            '{td.codigo}',
            '{td.nombre}',
            '{td.esquema_control}'
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/updatetipodispositivo")
def update_tipo_dispositivo(td: TipoDispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        CALL actualizar_tipo_dispositivo(
            {td.id_tipo},
            '{td.codigo}',
            '{td.nombre}',
            '{td.esquema_control}'
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}


@router.post("/deltipodispositivo")
def delete_tipo_dispositivo(td: TipoDispositivo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"CALL eliminar_tipo_dispositivo({td.id_tipo})")

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "1"}
