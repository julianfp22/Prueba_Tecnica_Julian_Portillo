# Prueba Técnica QA – Julián Portillo

| Carpeta | Contenido |
|---|---|
| `Prueba funcional/` | Casos de prueba, criterios, backlog, proceso de QA y evidencias de errores. Enlace al tablero Jira en `Enlace Tablero en Jira.txt`. |
| `Prueba API Postman/` | Evidencias de las pruebas de API en Postman. |
| `Prueba API python/` | Automatización de API (ReqRes) con Python + pytest + requests. |
| `saucedemo-smoke-selenium/` | Smoke test de login de SauceDemo con Selenium + pytest (Page Object Model). |

## Requisitos
- Python 3.10 o superior
- Google Chrome (solo para SauceDemo; el driver se descarga solo)

## Ejecutar la automatización de API
```powershell
cd "Prueba API python"
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
pytest
```
Si la API responde 401/403, crea una clave gratuita en https://app.reqres.in y define
`REQRES_API_KEY` (PowerShell: `$env:REQRES_API_KEY = "tu_clave"`). Resultado esperado: API-06 aparece como `xfailed` (ver README de la carpeta).

## Ejecutar el smoke test de SauceDemo
```powershell
cd saucedemo-smoke-selenium
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest                # con ventana; usa --headless para ocultarla
```

Cada ejecución regenera `reports/reporte.html`. Detalle de los casos en los `CASOS_DE_PRUEBA.md` de cada proyecto.
