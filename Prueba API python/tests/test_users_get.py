"""GET /users – consulta de usuarios (API-07 a API-09)."""
import pytest
from jsonschema import validate

from data import datos_prueba as datos
from schemas.user_schema import USUARIO_SCHEMA

pytestmark = pytest.mark.api


def test_api07_usuario_existente_cumple_el_esquema(api):
    # 1. Enviar GET a /users/2
    respuesta = api.obtener_usuario(datos.USUARIO_EXISTENTE_ID)

    # Resultado esperado: código 200
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    # Resultado esperado: la estructura cumple el esquema
    validate(instance=cuerpo, schema=USUARIO_SCHEMA)
    # Resultado esperado: data.id es 2
    assert cuerpo["data"]["id"] == datos.USUARIO_EXISTENTE_ID


def test_api08_usuario_inexistente_retorna_404(api):
    # 1. Enviar GET a /users/23
    respuesta = api.obtener_usuario(datos.USUARIO_INEXISTENTE_ID)

    # Resultado esperado: código 404
    assert respuesta.status_code == 404, (
        f"Se esperaba 404 y llegó {respuesta.status_code}: {respuesta.text}"
    )


def test_api09_listado_paginado(api):
    # 1. Enviar GET a /users?page=2
    respuesta = api.listar_usuarios(page=2)

    # Resultado esperado: código 200
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    # Resultado esperado: page es 2
    assert cuerpo["page"] == 2
    # Resultado esperado: data es una lista con al menos un usuario
    assert isinstance(cuerpo["data"], list) and len(cuerpo["data"]) > 0
