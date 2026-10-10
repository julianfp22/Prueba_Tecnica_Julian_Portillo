# Pruebas funcionales de API – ReqRes (`/users`)

Automatización con **Python + pytest + requests** de la API https://reqres.in/api/.
Los casos están diseñados en [CASOS_DE_PRUEBA.md](CASOS_DE_PRUEBA.md).

## Alcance

**Requerido por el enunciado**

| ID | Prueba |
|---|---|
| API-01 | `POST /users` con `{"name": "Test User", "job": "Automation Engineer"}` responde 201 |
| API-06 | Flujo: POST → extraer `id` → `GET /users/{id}` → 200 y `name`/`job` iguales a los enviados |

**Casos adicionales**

| ID | Prueba |
|---|---|
| API-02 | La respuesta del POST refleja `name` y `job` e incluye `id` y `createdAt` (ISO 8601) |
| API-03 | Datos variados (acentos, caracteres especiales, 200 caracteres) se reflejan sin alterarse |
| API-04 | Dos POST seguidos generan ids distintos |
| API-05 | Respuesta en JSON y en menos de 5 s |
| API-07 | `GET /users/2` → 200 y estructura validada con JSON Schema |
| API-08 | `GET /users/23` → 404 |
| API-09 | `GET /users?page=2` → 200, página 2 y datos presentes |
| API-10 | `PUT /users/2` → 200, datos reflejados y `updatedAt` |
| API-11 | `DELETE /users/2` → 204 sin contenido |

## Hallazgo importante: API-06

La documentación de ReqRes indica que `POST /users` es **"echoed, not persisted"**: devuelve lo
que se envía con un `id` y `createdAt`, pero **no guarda el usuario**. Por eso el paso del
enunciado "consultar el usuario recién creado y esperar 200" no se puede cumplir contra la API
pública, y se espera un 404.

Decisión tomada: la prueba API-06 implementa el flujo tal como lo pide el enunciado y está marcada
como `xfail` (fallo esperado, no estricto):

- Mientras la API no persista, aparece como **XFAIL** en el reporte con la razón documentada.
- Si algún día la API persiste, aparece como **XPASS**, que avisa de que el comportamiento cambió.
- Para convertirla en una prueba normal, basta quitar el decorador `@pytest.mark.xfail` de
  `tests/test_users_flow.py`.

Para persistencia real ReqRes ofrece `/api/collections/*` con una API key de cuenta gratuita; queda
fuera del alcance de este ejercicio.

## Requisitos

- Python 3.10 o superior

## Instalación

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## API key (si la API la pide)

La documentación de ReqRes no es consistente sobre si exige la cabecera `x-api-key`. Si al ejecutar
recibes un 401 o 403, el proyecto se detiene con un mensaje explicativo. En ese caso crea una clave
gratuita en https://app.reqres.in y defínela:

```powershell
$env:REQRES_API_KEY = "tu_clave"      # PowerShell
```
```bash
set REQRES_API_KEY=tu_clave           # CMD
export REQRES_API_KEY=tu_clave        # macOS / Linux
```

La clave nunca se escribe en el código ni se sube al repositorio.

## Ejecución

```bash
pytest                       # Todas las pruebas
pytest -k api06              # Solo el flujo POST -> GET
pytest -m api                # Solo las marcadas como api
```

Esperado contra la API pública: pasan las pruebas que dependen de comportamiento estándar y
API-06 aparece como `xfailed`.

## Reporte

`reports/reporte.html` se genera en cada ejecución. Ábrelo con `start reports\reporte.html`.

## Estructura

```
reqres-api-tests/
├── CASOS_DE_PRUEBA.md          Diseño de los casos
├── conftest.py                 Cliente de la API y comprobación previa de disponibilidad
├── pytest.ini                  Configuración de pytest y reporte HTML
├── requirements.txt            Dependencias
├── api/
│   └── users_client.py         Cliente HTTP: URLs, cabeceras y timeout en un solo lugar
├── data/
│   └── datos_prueba.py         Datos de prueba
├── schemas/
│   └── user_schema.py          JSON Schema de GET /users/{id}
└── tests/
    ├── test_users_post.py          API-01 a API-05
    ├── test_users_flow.py          API-06
    ├── test_users_get.py           API-07 a API-09
    └── test_users_update_delete.py API-10 y API-11
```

## Buenas prácticas aplicadas

- **Capa de cliente:** las pruebas no construyen URLs ni cabeceras; usan `UsersClient`.
- **Datos separados del código** y sin credenciales en el repositorio (API key por variable de entorno).
- **Validación de estructura** con JSON Schema, no solo del código de estado.
- **Mensajes de error útiles:** cada aserción incluye el código y el cuerpo recibidos.
- **Pruebas independientes:** ninguna depende del resultado de otra.
- **Timeout en todas las llamadas** para que una API caída no cuelgue la ejecución.
- **Fallo esperado documentado** (`xfail` con razón) en lugar de ocultar o forzar un resultado.
- **Trazabilidad:** cada prueba lleva el ID de su caso y comenta pasos y resultados esperados.
