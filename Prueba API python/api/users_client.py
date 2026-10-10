"""Cliente de la API de usuarios de ReqRes.

Concentra las llamadas HTTP (URL, cabeceras, timeout) para que las pruebas
solo describan qué se envía y qué se espera, sin repetir detalles de transporte.
"""
import requests

USER_AGENT = "Mozilla/5.0 (compatible; reqres-api-tests/1.0)"


class UsersClient:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )
        if api_key:
            self.session.headers["x-api-key"] = api_key

    def _url(self, ruta: str) -> str:
        return f"{self.base_url}{ruta}"

    def crear_usuario(self, datos: dict) -> requests.Response:
        return self.session.post(self._url("/users"), json=datos, timeout=self.timeout)

    def obtener_usuario(self, user_id) -> requests.Response:
        return self.session.get(self._url(f"/users/{user_id}"), timeout=self.timeout)

    def listar_usuarios(self, page: int | None = None) -> requests.Response:
        params = {"page": page} if page is not None else None
        return self.session.get(self._url("/users"), params=params, timeout=self.timeout)

    def actualizar_usuario(self, user_id, datos: dict) -> requests.Response:
        return self.session.put(self._url(f"/users/{user_id}"), json=datos, timeout=self.timeout)

    def eliminar_usuario(self, user_id) -> requests.Response:
        return self.session.delete(self._url(f"/users/{user_id}"), timeout=self.timeout)

    def cerrar(self):
        self.session.close()
