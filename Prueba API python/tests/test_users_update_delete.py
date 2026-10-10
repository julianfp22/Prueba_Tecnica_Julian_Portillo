"""PUT y DELETE /users/{id} (API-10 y API-11)."""
import pytest

from data import datos_prueba as datos

pytestmark = pytest.mark.api


def test_api10_actualizar_usuario(api):
    # 1. Enviar PUT a /users/2 con los datos actualizados
    respuesta = api.actualizar_usuario(datos.USUARIO_EXISTENTE_ID, datos.USUARIO_ACTUALIZADO)

    # Resultado esperado: código 200
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    # Resultado esperado: name y job reflejan lo enviado
    assert cuerpo["name"] == datos.USUARIO_ACTUALIZADO["name"]
    assert cuerpo["job"] == datos.USUARIO_ACTUALIZADO["job"]
    # Resultado esperado: la respuesta incluye updatedAt
    assert "updatedAt" in cuerpo, f"La respuesta no trae updatedAt: {cuerpo}"


def test_api11_eliminar_usuario(api):
    # 1. Enviar DELETE a /users/2
    respuesta = api.eliminar_usuario(datos.USUARIO_EXISTENTE_ID)

    # Resultado esperado: código 204
    assert respuesta.status_code == 204, (
        f"Se esperaba 204 y llegó {respuesta.status_code}: {respuesta.text}"
    )
    # Resultado esperado: cuerpo vacío
    assert respuesta.text == ""
