"""Page Object de la pantalla de inicio de sesión."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Localizadores
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_CONTRASENA = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, base_url: str):
        super().__init__(driver)
        self.base_url = base_url

    def abrir(self) -> "LoginPage":
        self.ir_a(self.base_url)
        self.esperar_visible(self.BOTON_LOGIN)
        return self

    def iniciar_sesion(self, usuario: str, contrasena: str):
        """Llena solo los campos con valor; un campo vacío se deja sin tocar."""
        if usuario:
            self.escribir(self.CAMPO_USUARIO, usuario)
        if contrasena:
            self.escribir(self.CAMPO_CONTRASENA, contrasena)
        self.hacer_clic(self.BOTON_LOGIN)

    def obtener_mensaje_error(self) -> str:
        return self.obtener_texto(self.MENSAJE_ERROR)

    def sigue_en_login(self) -> bool:
        return self.url_actual.rstrip("/") == self.base_url.rstrip("/") and self.esta_visible(
            self.BOTON_LOGIN
        )
