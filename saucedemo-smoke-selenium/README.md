# Smoke Test de Inicio de Sesión – SauceDemo

Automatización del smoke test de login de https://www.saucedemo.com/ con **Selenium + Python + pytest**, usando el patrón **Page Object Model (POM)**.

## Alcance cubierto

| ID | Escenario | Prueba |
|---|---|---|
| SMK-01 | Login exitoso con credenciales válidas | `test_smk01_login_exitoso_con_credenciales_validas` |
| SMK-02 | Login fallido con contraseña incorrecta | `test_smk02_login_fallido_con_contrasena_incorrecta` |
| SMK-03 | Campos obligatorios: usuario vacío | `test_validacion_campos_obligatorios[smk03_usuario_vacio]` |
| SMK-04 | Campos obligatorios: contraseña vacía | `test_validacion_campos_obligatorios[smk04_contrasena_vacia]` |
| SMK-05 | Campos obligatorios: ambos vacíos | `test_validacion_campos_obligatorios[smk05_ambos_vacios]` |

El diseño detallado de cada caso (precondiciones, pasos y resultados esperados) está en [CASOS_DE_PRUEBA.md](CASOS_DE_PRUEBA.md).

## Requisitos

- Python 3.10 o superior
- Google Chrome (también funciona con Firefox o Edge)
- No hace falta descargar el driver: Selenium Manager lo hace automáticamente

## Instalación

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Ejecución

Con el entorno virtual activado (`venv\Scripts\activate`; el prompt muestra `(venv)`) y desde la carpeta del proyecto:

```bash
pytest                          # Todas las pruebas en Chrome, con ventana visible
pytest --headless               # Sin abrir la ventana del navegador
pytest --browser firefox        # En Firefox (también: edge)
pytest -m smoke                 # Solo las pruebas marcadas como smoke
pytest -k smk02                 # Una sola prueba por nombre
pytest -n 2                     # En paralelo con 2 procesos (pytest-xdist)
pytest -n auto --headless       # En paralelo, un proceso por núcleo disponible
```

Sin activar el entorno, también se puede ejecutar directamente con su Python:

```bash
venv\Scripts\python.exe -m pytest -n 4      # Windows
```

> **Opcional (Windows, PowerShell):** para escribir solo `pytest -n 4` sin activar el entorno en cada terminal nueva, se puede definir una función `pytest` en el perfil de PowerShell (`$PROFILE`) que use el `venv` de la carpeta actual. Es una configuración personal del equipo y no forma parte del proyecto.

Las dependencias están fijadas en `requirements.txt` (`selenium`, `pytest`, `pytest-html`, `pytest-xdist`) para que los resultados sean reproducibles. Las pruebas se verificaron con Python 3.14 y Chrome en modo headless en paralelo.

## Reportes

- **Reporte HTML:** `reports/reporte.html` (se genera en cada ejecución)
- **Capturas de pantalla:** `reports/screenshots/`, solo cuando una prueba falla

## Estructura

```
saucedemo-smoke-selenium/
├── CASOS_DE_PRUEBA.md        Diseño de los casos manuales
├── conftest.py               Navegador (fixture), opciones de ejecución y capturas en fallos
├── pytest.ini                Configuración de pytest y reporte HTML
├── requirements.txt          Dependencias
├── data/
│   └── datos_prueba.py       Usuarios, contraseñas y mensajes esperados
├── pages/
│   ├── base_page.py          Acciones comunes con esperas explícitas
│   ├── login_page.py         Page Object del login
│   └── inventory_page.py     Page Object de la página de productos
└── tests/
    └── test_login_smoke.py   Pruebas del smoke test
```

## Buenas prácticas aplicadas

- **Page Object Model:** los localizadores y acciones viven en `pages/`; las pruebas solo describen pasos y verificaciones. Si cambia un elemento, se corrige en un solo lugar.
- **Esperas explícitas:** `WebDriverWait` con condiciones esperadas. No hay `time.sleep` ni esperas implícitas.
- **Localizadores estables:** `id` y atributos `data-test` de la aplicación, en lugar de XPath largos.
- **Datos separados del código:** credenciales y mensajes esperados en `data/datos_prueba.py`.
- **Pruebas independientes:** cada prueba abre su propio navegador y lo cierra al terminar.
- **Parametrización:** los tres escenarios de campos obligatorios comparten una sola prueba con datos distintos.
- **Trazabilidad:** cada prueba lleva el ID de su caso y comenta los pasos y resultados esperados.
- **Evidencia:** reporte HTML y captura de pantalla automática en cada fallo.
- **Ejecución flexible:** navegador y modo headless configurables por línea de comandos; URL configurable con la variable de entorno `BASE_URL`.
