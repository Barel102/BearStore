from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.HomePage import MainPage
from Pages.ItemsPage import ItemsPage
from Pages.ItemPage import ItemPage
from Pages.LoginPage import LoginPage
from Pages.ShoppingBasket import Basket
from Pages.Cart import Cart
from time import sleep


class TestItemCategoryTitle(TestCase):
    def setUp(self):
        # Initialize browser and navigate to the website

        self.driver = webdriver.Chrome()
        self.driver.get("https://bearstore-testsite.smartbear.com/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

        # Initialize page objects
        self.home_page = MainPage(self.driver)
        self.items_page = ItemsPage(self.driver)
        self.item_page = ItemPage(self.driver)
        self.basket = Basket(self.driver)
        self.cart = Cart(self.driver)
        self.login_logout = LoginPage(self.driver)
        self.addCleanup(self.driver.quit)

    def test_1(self):
        # Select a random category from the homepage
        random_category_item = self.home_page.random_category()
        random_category_item_name = random_category_item.text.strip()
        random_category_item.click()
        sub_category_title = self.items_page.items_title()

        self.assertEqual(random_category_item_name, sub_category_title)

        random_item = self.items_page.random_items()
        random_item_name = self.items_page.random_item_title(random_item)
        self.items_page.random_item_click(random_item)

        item_page_title = self.item_page.item_title()

        self.assertEqual(random_item_name, item_page_title)

        self.driver.back()

        sub_category_title = self.items_page.items_title()

        self.assertEqual(random_category_item_name, sub_category_title)

        self.driver.back()

        self.assertEqual(self.driver.current_url, 'https://bearstore-testsite.smartbear.com/')

    def test_2(self):
        self.home_page.random_category().click()

        self.items_page.random_items().click()

        amount1 = self.item_page.randomize_amount()

        self.item_page.add_to_cart().click()

        self.driver.back()

        self.driver.back()

        self.home_page.random_category().click()

        self.items_page.random_items().click()

        amount2 = self.item_page.randomize_amount()

        self.item_page.add_to_cart().click()

        item_count = self.basket.cart_item_count_icon()

        self.assertEqual(str(amount1 + amount2), item_count)
        sleep(2)

    def test_3(self):
        for _ in range(3):
            random_category_item = self.home_page.random_category()
            random_category_item.click()
            random_item = self.items_page.random_items()
            random_item_name1 = self.items_page.random_item_title(random_item)
            self.items_page.random_item_click(random_item)

            item_price = self.item_page.get_price()
            amount1 = self.item_page.randomize_amount()

            self.item_page.add_to_cart()

            cart_items = self.basket.cart_item_list()

            first_item = cart_items[0]

            sleep(2)
            item_name = self.basket.get_item_name(first_item)
            item_price_cart = self.basket.get_item_price(first_item)
            item_quantity_cart = self.basket.get_item_quantity(first_item)

            print(f"Expected Name: {random_item_name1}, Cart Name: {item_name}")
            print(f"Expected Price: {item_price}, Cart Price: {item_price_cart}")
            print(f"Expected Amount: {amount1}, Cart Amount: {item_quantity_cart}")

            # Fix for type mismatch: Ensure item_count is an integer
            self.assertEqual(random_item_name1, item_name)
            self.assertEqual(item_price, item_price_cart)
            self.assertEqual(str(amount1), item_quantity_cart)

            self.driver.get("https://bearstore-testsite.smartbear.com/")


    def test_4(self):
        global item_price1
        self.basket.item_bag_icon().click()
        self.driver.get("https://bearstore-testsite.smartbear.com/")
        for _ in range(2):
            random_category_item = self.home_page.random_category()
            random_category_item.click()
            random_item = self.items_page.random_items()
            self.items_page.random_item_click(random_item)
            item_price1 = self.item_page.get_price()


            self.item_page.add_to_cart()

            self.driver.get("https://bearstore-testsite.smartbear.com/")

        self.basket.item_bag_icon().click()

        items_count_before_delete = self.basket.cart_items_list_count()
        total_price_before_delete = float(self.basket.total_price())

        self.basket.remove_item(self.basket.cart_item_list()[-1])
        sleep(2)

        items_count_after_delete = self.basket.cart_items_list_count()
        total_price_after_delete = float(self.basket.total_price())

        print(len(items_count_before_delete))
        print(len(items_count_after_delete))
        item_price = float(''.join([char for char in item_price1 if char.isdigit() or char == '.']))
        self.assertEqual(1, len(items_count_before_delete) - len(items_count_after_delete))
        self.assertEqual(total_price_after_delete, total_price_before_delete - item_price)

    def test5(self):
        random_category_item = self.home_page.random_category()
        random_category_item.click()
        random_item = self.items_page.random_items()
        self.items_page.random_item_click(random_item)
        self.item_page.add_to_cart()
        canvas = self.basket.canvas_overlay()
        sleep(2)
        self.assertTrue(canvas.is_displayed(), "Cart is hidden")
        sleep(2)
        self.driver.find_element(By.CLASS_NAME, "canvas-blocker").click()

        sleep(2)
        self.assertFalse(canvas.is_displayed(), "Cart is visible")
        sleep(2)
        self.basket.item_bag_icon().click()
        sleep(2)
        self.assertTrue(canvas.is_displayed(), "Cart is hidden")
        sleep(2)
        self.basket.go_to_cart().click()

        self.assertEqual(self.driver.current_url, "https://bearstore-testsite.smartbear.com/cart")



    def test6(self):
        total_expected_price = 0
        cart_items = []

        for _ in range(3):  # Add 3 different products
            random_category_item = self.home_page.random_category()
            random_category_item.click()
            random_item = self.items_page.random_items()
            random_item_name = self.items_page.random_item_title(random_item)
            self.items_page.random_item_click(random_item)
            item_price = float(''.join([char for char in self.item_page.get_price() if char.isdigit() or char == '.']))

            # Convert price to float
            amount = self.item_page.randomize_amount()  # Get randomized quantity
            self.item_page.add_to_cart()

            total_expected_price += item_price * amount
            cart_items.append((random_item_name, amount, item_price))

            self.driver.get("https://bearstore-testsite.smartbear.com/")  # Go back to home

        self.basket.item_bag_icon().click()
        sleep(2)

        total_cart_price = float(self.basket.total_price())

        for name, quantity, price in cart_items:
            print(f"Product: {name}, Quantity: {quantity}, Price per item: {price}")

        print(f"Expected Total Price: {total_expected_price}, Cart Total Price: {total_cart_price}")

        self.assertEqual(total_expected_price, total_cart_price, "Total cart price does not match expected price")

    def test7(self):
        total_expected_price = 0
        cart_items = []

        # Step 1: Add two different products to the cart
        for _ in range(2):
            self.driver.get("https://bearstore-testsite.smartbear.com/")
            random_category_item = self.home_page.random_category()
            random_category_item.click()
            random_item = self.items_page.random_items()
            self.items_page.random_item_click(random_item)
            random_item_amount = self.item_page.randomize_amount()
            random_item_price = self.item_page.get_price()
            self.item_page.add_to_cart()
            cart_items.insert(0, (random_item_price, random_item_amount))

        self.basket.go_to_cart().click()

        for i in range(len(cart_items)):
            self.basket.increase_product_quantity()[i].click()
            sleep(2)

        list_total_price_items = self.cart.get_total_prices_from_items()

        for i in range(len(list_total_price_items)):
            expected_total = cart_items[i][0] * (cart_items[i][1] + 1)
            print(f'{i}: {cart_items[i][0]} : {cart_items[i][1]} : {list_total_price_items}')# price * quantity
            self.assertEqual(round(list_total_price_items[i], 2), round(expected_total, 2))

        overall_price = self.cart.total_price()
        self.assertEqual(round(overall_price, 2),round(sum(list_total_price_items),2))

        self.driver.get("https://bearstore-testsite.smartbear.com/")

        sleep(2)
        self.basket.item_bag_icon().click()
        sleep(2)

        total_price_in_basket = self.basket.total_price()

        self.assertEqual(overall_price, total_price_in_basket)

    def test_9(self):

        # Click on the button to navigate to the login page
        self.login_logout.login_page_button().click()
        sleep(2)

        # Enter username and password
        self.login_logout.username_login_button().send_keys("katebarellol555")
        self.login_logout.password_login_button().send_keys("Kff1234567890")

        # Click on the login button
        self.login_logout.login_button_in_login_page().click()
        sleep(2)

        # Verify login success by checking if the 'username' button is displayed
        assert self.assertTrue(self.login_logout.login_button_in_login_page().is_displayed(), "Login failed")
        print("Login successful!")

        # Perform logout
        self.login_logout.username_button().click()
        self.login_logout.log_out_button().click()
        sleep(2)

        # Verify logout success by checking if the 'login' button is displayed again
        assert self.assertFalse(self.login_logout.login_page_button().is_displayed(), "Logout failed")

    def test996(self):
        sleep(10000)


