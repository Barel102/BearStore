from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Cart:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

    def get_total_prices_from_items(self):  #Fixed `self`
        """ Retrieves all total price elements that belong to data-caption='Total'. """
        total_price_containers = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-caption='Total']"))
        )

        total_prices = []
        for container in total_price_containers:
            try:
                price_element = container.find_element(By.CLASS_NAME, "price")
                price_text = price_element.text  # Example: "$59.98 excl tax"

                #Extract only numeric values from the price text
                total_price = float(''.join([c for c in price_text if c.isdigit() or c == "."]))
                total_prices.append(total_price)
            except Exception:
                print("Price element not found inside a 'Total' container!")

        return total_prices

    def total_price(self):
        """ Retrieves the subtotal price from the cart summary. """
        try:
            #Locate the correct subtotal element using 'cart-summary-value'
            sub_total_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "cart-summary-value"))
            )

            # Extract the text (Example: "$1,809.05 excl tax")
            sub_total_text = sub_total_element.text

            # Remove non-numeric characters except '.' and ','
            sub_total_cleaned = ''.join([c for c in sub_total_text if c.isdigit() or c in [".", ","]])

            # Convert to float (replace ',' with empty string for thousands)
            total_price = float(sub_total_cleaned.replace(",", ""))

            print(f" DEBUG: Total cart price detected: {total_price}")  # Debugging
            return total_price
        except Exception as e:
            print(f" ERROR: Could not find total price! Check locator. Error: {e}")
            return None  # Prevent crashes

