"""Smoke Test de Inicio de Sesión – SauceDemo.

Cada prueba corresponde a un caso de CASOS_DE_PRUEBA.md.
"""
import pytest

from data import datos_prueba as datos
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.smoke


def test_smk01_login_exitoso_con_credenciales_validas(driver, base_url):
    # 1. Abrir la página de login
    login = LoginPage(driver, base_url).abrir()
    # 2-4. Escribir usuario y contraseña válidos y clic en "Login"
    login.iniciar_sesion(datos.USUARIO_VALIDO, datos.CONTRASENA_VALIDA)

    inventario = InventoryPage(driver)
    # Resultado esperado: redirige a la página de productos
    assert inventario.esta_cargada(), (
        f"No redirigió a {InventoryPage.RUTA}. URL actual: {inventario.url_actual}"
    )
    # Resultado esperado: se muestra el título "Products"
    assert inventario.obtener_titulo() == datos.TITULO_INVENTARIO
    # Resultado esperado: se muestra la lista de productos
    assert inventario.lista_productos_visible(), "La lista de productos no está visible"


def test_smk02_login_fallido_con_contrasena_incorrecta(driver, base_url):
    # 1. Abrir la página de login
    login = LoginPage(driver, base_url).abrir()
    # 2-4. Usuario válido, contraseña incorrecta y clic en "Login"
    login.iniciar_sesion(datos.USUARIO_VALIDO, datos.CONTRASENA_INVALIDA)

    # Resultado esperado: se muestra el mensaje de credenciales inválidas
    assert login.obtener_mensaje_error() == datos.MSG_CREDENCIALES_INVALIDAS
    # Resultado esperado: el usuario permanece en la página de login
    assert login.sigue_en_login(), f"Salió de la página de login. URL actual: {login.url_actual}"


@pytest.mark.parametrize(
    "usuario, contrasena, mensaje_esperado",
    [
        ("", datos.CONTRASENA_VALIDA, datos.MSG_USUARIO_REQUERIDO),  # SMK-03
        (datos.USUARIO_VALIDO, "", datos.MSG_CONTRASENA_REQUERIDA),  # SMK-04
        ("", "", datos.MSG_USUARIO_REQUERIDO),  # SMK-05
    ],
    ids=["smk03_usuario_vacio", "smk04_contrasena_vacia", "smk05_ambos_vacios"],
)
def test_validacion_campos_obligatorios(driver, base_url, usuario, contrasena, mensaje_esperado):
    # 1. Abrir la página de login
    login = LoginPage(driver, base_url).abrir()
    # 2-4. Dejar vacío el campo correspondiente y clic en "Login"
    login.iniciar_sesion(usuario, contrasena)

    # Resultado esperado: se muestra el mensaje del campo obligatorio
    assert login.obtener_mensaje_error() == mensaje_esperado
    # Resultado esperado: el usuario permanece en la página de login
    assert login.sigue_en_login(), f"Salió de la página de login. URL actual: {login.url_actual}"
