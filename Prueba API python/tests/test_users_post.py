"""POST /users – creación de usuarios (API-01 a API-05)."""
from datetime import datetime

import pytest

from data import datos_prueba as datos

pytestmark = pytest.mark.api


def _es_fecha_iso(texto) -> bool:
    try:
        datetime.fromisoformat(str(texto).replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def test_api01_crear_usuario_retorna_201(api):
    # 1. Enviar POST a /users con los datos de prueba
    respuesta = api.crear_usuario(datos.USUARIO)

    # Resultado esperado: código 201
    assert respuesta.status_code == 201, (
        f"Se esperaba 201 y llegó {respuesta.status_code}: {respuesta.text}"
    )


def test_api02_respuesta_refleja_datos_e_incluye_id_y_fecha(api):
    # 1. Enviar POST a /users con los datos de prueba
    respuesta = api.crear_usuario(datos.USUARIO)
    assert respuesta.status_code == 201, respuesta.text
    cuerpo = respuesta.json()

    # Resultado esperado: name y job iguales a los enviados
    assert cuerpo["name"] == datos.USUARIO["name"]
    assert cuerpo["job"] == datos.USUARIO["job"]
    # Resultado esperado: id no vacío
    assert str(cuerpo.get("id", "")).strip() != "", f"La respuesta no trae id: {cuerpo}"
    # Resultado esperado: createdAt con formato de fecha ISO 8601
    assert _es_fecha_iso(cuerpo.get("createdAt")), f"createdAt inválido: {cuerpo.get('createdAt')}"


@pytest.mark.parametrize(
    "nombre, trabajo", datos.DATOS_VARIADOS, ids=datos.IDS_DATOS_VARIADOS
)
def test_api03_datos_variados_se_reflejan_sin_alterarse(api, nombre, trabajo):
    # 1. Enviar POST a /users con datos variados
    respuesta = api.crear_usuario({"name": nombre, "job": trabajo})

    # Resultado esperado: código 201
    assert respuesta.status_code == 201, respuesta.text
    cuerpo = respuesta.json()
    # Resultado esperado: name y job idénticos a lo enviado
    assert cuerpo["name"] == nombre
    assert cuerpo["job"] == trabajo


def test_api04_dos_creaciones_generan_ids_distintos(api):
    # 1. Enviar POST a /users con los datos de prueba
    primera = api.crear_usuario(datos.USUARIO)
    # 2. Enviar de nuevo el mismo POST
    segunda = api.crear_usuario(datos.USUARIO)

    # Resultado esperado: ambas respuestas son 201
    assert primera.status_code == 201, primera.text
    assert segunda.status_code == 201, segunda.text
    # Resultado esperado: los dos id son distintos
    assert primera.json()["id"] != segunda.json()["id"]


def test_api05_respuesta_es_json_y_rapida(api):
    # 1. Enviar POST a /users con los datos de prueba
    respuesta = api.crear_usuario(datos.USUARIO)

    # Resultado esperado: Content-Type contiene application/json
    assert "application/json" in respuesta.headers.get("Content-Type", "")
    # Resultado esperado: responde en menos de 5 segundos
    segundos = respuesta.elapsed.total_seconds()
    assert segundos < datos.TIEMPO_MAXIMO_S, f"Tardó {segundos:.2f} s"
