from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Basket:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Global WebDriverWait instance

    def cart_item_count_icon(self):
        """ Waits for and retrieves the number of items in the cart. """
        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#cart-tab > span.badge.badge-pill.label-cart-amount.badge-warning"))
        )
        total_quantity = self.wait.until(EC.presence_of_element_located((By.ID, "cart-tab")))
        return total_quantity.find_elements(By.TAG_NAME, "span")[1].text

    def cart_item_list(self):
        """ Retrieves all cart items, ensuring they are fully loaded. """
        return self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'offcanvas-cart-item')))

    def get_item_name(self, item):
        """ Retrieves the item name from a given cart item element. """
        return item.find_element(By.CLASS_NAME, "pd-name").text

    def get_item_price(self, item):
        """ Retrieves the price of a specific cart item element. """
        return item.find_element(By.CLASS_NAME, "unit-price").text

    def get_item_quantity(self, item):
        """ Retrieves the quantity of a specific cart item element. """
        return item.find_element(By.ID, "item_EnteredQuantity").get_attribute("value")

    def cart_items_list_count(self):
        """ Retrieves the count of items in the cart. """
        return self.driver.find_elements(By.CLASS_NAME, 'offcanvas-cart-item')

    def remove_item(self, item):
        """ Removes a specific item from the cart. """
        item.find_element(By.CSS_SELECTOR, "[title='Remove']").click()

    def total_price(self):
        """ Waits for and retrieves the total price of items in the cart. """

        #Locate the correct subtotal element using 'sub-total price'
        sub_total_element = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "sub-total price"))
        )

        # Extract the text (Example: "$1,809.05 excl tax")
        sub_total_text = sub_total_element.text

        # Remove non-numeric characters except '.' and ','
        sub_total_cleaned = ''.join([c for c in sub_total_text if c.isdigit() or c in [".", ","]])

        # Convert to float (replace ',' with empty string for thousands)
        total_price = float(sub_total_cleaned.replace(",", ""))

        print(f"DEBUG: Total cart price detected: {total_price}")  # Debugging
        return total_price

    def canvas_overlay(self):
        """ Waits for and retrieves the cart overlay element. """
        return self.wait.until(
            EC.presence_of_element_located((By.ID, "offcanvas-cart"))
        )

    def item_bag_icon(self):
        """ Waits for and retrieves the shopping bag icon element. """
        return self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.icm.icm-bag'))
        )

    def go_to_cart(self):
        """ Waits for and retrieves the 'Go to Cart' button. """
        return self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "Go to cart"))
        )

    def increase_product_quantity(self):
        """ Waits for and retrieves all 'increase quantity' buttons. """
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fa-plus"))
        )

    def decrease_product_quantity(self):
        """ Waits for and retrieves all 'decrease quantity' buttons. """
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fa-minus"))
        )

    def quantity_value(self):
        """ Waits for and retrieves all quantity input fields in the cart. """
        container = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart-body"))
        )
        return container.find_elements(By.CLASS_NAME, "form-control")
