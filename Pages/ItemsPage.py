from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class ItemsPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

    def items_title(self):
        # Wait for the h1 element to be present and return its text
        return self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1"))).text

    def random_items(self):
        """ Selects a random item from the product list. """
        items_container = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-list-container"))
        )
        items = items_container.find_elements(By.CLASS_NAME, "art")

        if not items:
            raise Exception("No items found inside the product list!")
        selected_item = random.choice(items)
        return selected_item

    def random_item_title(self, item):
        # Ensure the item's title link is present and return its text
        random_item_title = self.wait.until(
            EC.presence_of_element_located((By.XPATH, ".//h3[@class='art-name']/a"))
        )
        return random_item_title.text

    def random_item_click(self, item):
        # Ensure the clickable element is available before clicking
        clickable_item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, ".//h3[@class='art-name']/a"))
        )
        clickable_item.click()
