"""Page Object de la página de productos (destino después de un login exitoso)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    RUTA = "/inventory.html"

    # Localizadores
    TITULO = (By.CLASS_NAME, "title")
    LISTA_PRODUCTOS = (By.CLASS_NAME, "inventory_list")

    def esta_cargada(self) -> bool:
        return self.url_contiene(self.RUTA)

    def obtener_titulo(self) -> str:
        return self.obtener_texto(self.TITULO)

    def lista_productos_visible(self) -> bool:
        return self.esta_visible(self.LISTA_PRODUCTOS)
