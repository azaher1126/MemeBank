from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_test_class import BaseTestClass

class AccountTests(BaseTestClass):
    def test_login_username(self):
        user_id = self.createTestUser()
        login_full_path = self.getFullWebPath("/login")
        self.driver.get(login_full_path)

        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.account-form input[type=submit]'))
        )

        username_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=username_or_email]")
        username = self.TEST_USERNAME_TEMPLATE.format(user_id)
        username_field.send_keys(username)

        password_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=password]")
        password_field.send_keys(self.TEST_USER_PASSWORD)

        login_button.click()

        wait = WebDriverWait(self.driver, 10).until(
            EC.url_changes(login_full_path)
        )

        self.assertTrue(wait)
        home_path = self.getFullWebPath('/')
        self.assertEqual(home_path, self.driver.current_url)

        username_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-menu .text-dropdown-item"))
        )

        self.assertTrue(self.pageFlashesContain(self.TEST_FIRST_NAME))
        self.assertEqual(username_text.get_attribute("innerText"), username)

    def test_login_email(self):
        user_id = self.createTestUser()
        login_full_path = self.getFullWebPath("/login")
        self.driver.get(login_full_path)

        login_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.account-form input[type=submit]'))
        )

        email_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=username_or_email]")
        email = self.TEST_USER_EMAIL_TEMPLATE.format(user_id)
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=password]")
        password_field.send_keys(self.TEST_USER_PASSWORD)

        login_button.click()

        wait = WebDriverWait(self.driver, 10).until(
            EC.url_changes(login_full_path)
        )

        self.assertTrue(wait)
        home_path = self.getFullWebPath('/')
        self.assertEqual(home_path, self.driver.current_url)

        username_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-menu .text-dropdown-item"))
        )

        self.assertTrue(self.pageFlashesContain(self.TEST_FIRST_NAME))
        username = self.TEST_USERNAME_TEMPLATE.format(user_id)
        self.assertEqual(username_text.get_attribute("innerText"), username)

    def test_login_from_nav_username(self):
        user_id = self.createTestUser()
        home_path = self.getFullWebPath('/')
        self.driver.get(home_path)

        dropdown_trigger = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.dropdown-toggle'))
        )

        dropdown_trigger.click()

        login_form = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dropdown-menu form'))
        )

        email_field = login_form.find_element(By.NAME, "username_or_email")
        email = self.TEST_USER_EMAIL_TEMPLATE.format(user_id)
        email_field.send_keys(email)

        password_field = login_form.find_element(By.NAME, "password")
        password_field.send_keys(self.TEST_USER_PASSWORD)

        login_button = login_form.find_element(By.TAG_NAME, "button")
        login_button.click()

        username_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-menu .text-dropdown-item"))
        )

        self.assertEqual(home_path, self.driver.current_url)
        self.assertTrue(self.pageFlashesContain(self.TEST_FIRST_NAME))
        username = self.TEST_USERNAME_TEMPLATE.format(user_id)
        self.assertEqual(username_text.get_attribute("innerText"), username)

    def test_login_from_nav_email(self):
        user_id = self.createTestUser()
        home_path = self.getFullWebPath('/')
        self.driver.get(home_path)

        dropdown_trigger = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.dropdown-toggle'))
        )

        dropdown_trigger.click()

        login_form = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.dropdown-menu form'))
        )

        username_field = login_form.find_element(By.NAME, "username_or_email")
        username = self.TEST_USERNAME_TEMPLATE.format(user_id)
        username_field.send_keys(username)

        password_field = login_form.find_element(By.NAME, "password")
        password_field.send_keys(self.TEST_USER_PASSWORD)

        login_button = login_form.find_element(By.TAG_NAME, "button")
        login_button.click()

        username_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-menu .text-dropdown-item"))
        )

        self.assertEqual(home_path, self.driver.current_url)
        self.assertTrue(self.pageFlashesContain(self.TEST_FIRST_NAME))
        self.assertEqual(username_text.get_attribute("innerText"), username)

    def test_register(self):
        register_full_path = self.getFullWebPath("/register")
        self.driver.get(register_full_path)

        register_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.account-form input[type=submit]'))
        )

        first_name_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=first_name]")
        first_name_field.send_keys(self.TEST_FIRST_NAME)

        last_name_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=last_name]")
        last_name_field.send_keys(self.TEST_LAST_NAME)

        username_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=username]")
        username = self.TEST_USERNAME_TEMPLATE.format(1)
        username_field.send_keys(username)

        email_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=email]")
        email = self.TEST_USER_EMAIL_TEMPLATE.format(1)
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=password]")
        password_field.send_keys(self.TEST_USER_PASSWORD)

        confirm_password_field = self.driver.find_element(By.CSS_SELECTOR, ".account-form input[name=confirm_password]")
        confirm_password_field.send_keys(self.TEST_USER_PASSWORD)

        register_button.click()

        wait = WebDriverWait(self.driver, 10).until(
            EC.url_changes(register_full_path)
        )

        self.assertTrue(wait)
        home_path = self.getFullWebPath('/')
        self.assertEqual(home_path, self.driver.current_url)

        username_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dropdown-menu .text-dropdown-item"))
        )

        self.assertTrue(self.pageFlashesContain(self.TEST_FIRST_NAME))
        self.assertEqual(username_text.get_attribute("innerText"), username)

    def test_logout(self):
        user_id = self.createTestUser()

        logout_full_path = self.getFullWebPath("/logout")
        with self.logged_in_context(user_id):
            self.driver.get(logout_full_path)

            wait = WebDriverWait(self.driver, 10).until(
                EC.url_changes(logout_full_path)
            )

            self.assertTrue(wait)

            home_path = self.getFullWebPath('/')
            self.assertEqual(self.driver.current_url, home_path)

            self.assertTrue(self.pageFlashesContain("logged out"))
            self.assertIsNotNone(self.driver.find_element(By.CSS_SELECTOR, ".dropdown-menu a.dropdown-item[href='/register']"))