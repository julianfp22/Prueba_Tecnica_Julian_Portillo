"""Configuración compartida: cliente de la API y comprobación previa de disponibilidad."""
import os

import pytest
import requests

from api.users_client import UsersClient

BASE_URL = os.getenv("BASE_URL", "https://reqres.in/api")
API_KEY = os.getenv("REQRES_API_KEY")


@pytest.fixture(scope="session")
def api():
    """Cliente único para toda la sesión. Antes de empezar comprueba que la API responde."""
    cliente = UsersClient(BASE_URL, API_KEY)

    try:
        respuesta = cliente.obtener_usuario(2)
    except requests.RequestException as error:
        pytest.exit(f"No se pudo conectar con {BASE_URL}: {error}", returncode=2)

    if respuesta.status_code in (401, 403):
        pytest.exit(
            f"La API respondió {respuesta.status_code}: {respuesta.text[:200]}\n"
            "Es probable que pida una API key. Crea una gratis en https://app.reqres.in y ejecuta:\n"
            "  PowerShell:  $env:REQRES_API_KEY = 'tu_clave'\n"
            "  CMD:         set REQRES_API_KEY=tu_clave",
            returncode=2,
        )

    yield cliente
    cliente.cerrar()
