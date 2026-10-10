"""Página base: acciones comunes con esperas explícitas (sin time.sleep)."""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def ir_a(self, url: str):
        self.driver.get(url)

    def esperar_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def escribir(self, locator, texto: str):
        elemento = self.esperar_visible(locator)
        elemento.clear()
        elemento.send_keys(texto)

    def hacer_clic(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def obtener_texto(self, locator) -> str:
        return self.esperar_visible(locator).text

    def esta_visible(self, locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def url_contiene(self, fragmento: str, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(fragmento))
            return True
        except TimeoutException:
            return False

    @property
    def url_actual(self) -> str:
        return self.driver.current_url
