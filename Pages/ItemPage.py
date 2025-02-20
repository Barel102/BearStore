from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

class ItemPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

    def item_title(self):
        title = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pd-name")))
        return title.text

    def amount_select(self):
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name*='AddToCart.EnteredQuantity']")))

    def randomize_amount(self):
        list_random_num = [i for i in range(1, 10)]
        num = random.choice(list_random_num)
        list_random_num.remove(num)

        amount_button = self.amount_select()
        amount_button.clear()
        amount_button.send_keys(str(num))
        return num

    def add_to_cart(self):
        add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart")))
        add_to_cart_button.click()

    def get_price(self):
        price_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="pd-form"]/section/aside/div[4]/div[1]/div/div[1]/div/div/div/span')
        )).text
        price = (''.join([char for char in price_element if char.isdigit() or char == '.']))
        price_clean = float(price.replace(",", ""))

        return price_clean
