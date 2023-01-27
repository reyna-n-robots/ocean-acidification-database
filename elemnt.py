from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        self.driver = driver
        try:
            elem = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, value))
            )
        finally:
            print("you found me")

    def __get__(self, obj, owner):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(self.locator)
        )
        element = driver.find_element(self.locator)
        return element.get_attribute("value")