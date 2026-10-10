"""Configuración compartida: creación del navegador y captura de pantalla en fallos."""
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Evita que Python genere carpetas __pycache__ en el proyecto
sys.dont_write_bytecode = True

INTENTOS_ARRANQUE = 3

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
CARPETA_CAPTURAS = Path(__file__).parent / "reports" / "screenshots"


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Navegador para ejecutar las pruebas",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar sin abrir la ventana del navegador",
    )


def _crear_driver(navegador: str, headless: bool):
    """Crea el WebDriver. Selenium Manager descarga el driver automáticamente."""
    if navegador == "chrome":
        opciones = webdriver.ChromeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1366,768")
        # Desactiva el aviso de "contraseña filtrada" de Chrome, que puede tapar la página
        opciones.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
        return webdriver.Chrome(options=opciones)

    if navegador == "firefox":
        opciones = webdriver.FirefoxOptions()
        if headless:
            opciones.add_argument("-headless")
        driver = webdriver.Firefox(options=opciones)
        driver.set_window_size(1366, 768)
        return driver

    opciones = webdriver.EdgeOptions()
    if headless:
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1366,768")
    return webdriver.Edge(options=opciones)


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def driver(request):
    """Un navegador nuevo por prueba: cada prueba es independiente."""
    navegador = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    # Reintento al arrancar: en paralelo (pytest -n), varios procesos pueden pedir
    # el driver al mismo tiempo la primera vez que Selenium Manager lo descarga.
    # Este sleep es solo de infraestructura; las pruebas usan esperas explícitas.
    for intento in range(1, INTENTOS_ARRANQUE + 1):
        try:
            driver = _crear_driver(navegador, headless)
            break
        except WebDriverException:
            if intento == INTENTOS_ARRANQUE:
                raise
            time.sleep(2)

    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Guarda una captura de pantalla cuando una prueba falla."""
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when == "call" and reporte.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
            nombre_seguro = re.sub(r"[^\w\-]", "_", item.name)
            archivo = CARPETA_CAPTURAS / f"{nombre_seguro}_{datetime.now():%Y%m%d_%H%M%S}.png"
            driver.save_screenshot(str(archivo))
