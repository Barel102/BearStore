from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

class MainPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

    def random_category(self):
        # Wait for the category container to be present
        category_container = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "artlist"))
        )

        # Wait for all category elements inside the container
        categories = category_container.find_elements(By.CLASS_NAME, "art")

        if not categories:
            raise Exception("No categories found on the page!")

        # Choose a random category
        random_category = random.choice(categories)

        return random_category



    def header_navbar(self):
        self.driver.find_element(By.CLASS_NAME, "menubar navbar navbar-slide")