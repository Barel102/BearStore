from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def login_page_button(self):
        return self.driver.find_element(By.ID, "menubar-my-account")

    def username_login_button(self):
        return self.driver.find_element(By.ID, "UsernameOrEmail")

    def password_login_button(self):
        return self.driver.find_element(By.ID, "Password")

    def login_button_in_login_page(self):
        return self.driver.find_element(By.XPATH, "//button[normalize-space()='Log in']")

    def username_button(self):
        return self.driver.find_element(By.CLASS_NAME,"fa-user-circle")

    def log_out_button(self):
        return self.driver.find_element(By.CLASS_NAME,"fa-sign-out-alt")

    def account_icon_text(self):
        account_icon_text = self.driver.find_element(By.CSS_SELECTOR,"#menubar-my-account > div > a > span")
        return account_icon_text.text

    def user_name_text(self):
        user_name = self.driver.find_element(By.CSS_SELECTOR,"#menubar-my-account > div > a > span")
        return user_name.text