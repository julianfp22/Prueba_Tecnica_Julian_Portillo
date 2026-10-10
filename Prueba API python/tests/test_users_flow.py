"""Flujo completo POST -> GET (API-06). Es el escenario principal del enunciado."""
import pytest

from data import datos_prueba as datos

pytestmark = pytest.mark.api


@pytest.mark.xfail(
    reason=(
        "Hallazgo conocido: la documentación de ReqRes indica que POST /users es "
        "'echoed, not persisted' (no guarda el usuario), por lo que se espera que "
        "GET /users/{id} del usuario recién creado responda 404 y no 200. "
        "Si la API empieza a persistir, la prueba aparecerá como XPASS."
    ),
    raises=AssertionError,
    strict=False,
)
def test_api06_crear_usuario_y_consultarlo_por_id(api):
    # 1. Enviar POST a /users con los datos de prueba
    respuesta_post = api.crear_usuario(datos.USUARIO)
    # Resultado esperado: el POST responde 201
    assert respuesta_post.status_code == 201, respuesta_post.text

    # 2. Extraer el id del usuario recién creado
    user_id = respuesta_post.json()["id"]

    # 3. Enviar GET a /users/{id} con ese id
    respuesta_get = api.obtener_usuario(user_id)
    # Resultado esperado: el GET responde 200
    assert respuesta_get.status_code == 200, (
        f"GET /users/{user_id} respondió {respuesta_get.status_code}: {respuesta_get.text}"
    )

    # Resultado esperado: name y job coinciden con lo enviado en el POST
    cuerpo = respuesta_get.json()
    usuario = cuerpo.get("data", cuerpo)
    assert usuario.get("name") == datos.USUARIO["name"]
    assert usuario.get("job") == datos.USUARIO["job"]
