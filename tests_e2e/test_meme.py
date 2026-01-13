import os
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_test_class import BaseTestClass


class MemeTests(BaseTestClass):
    def test_upload_meme(self):
        user_id = self.createTestUser()
        with self.logged_in_context(user_id):
            upload_path = self.getFullWebPath("/upload")
            self.driver.get(upload_path)

            upload_form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form.upload-form"))
            )

            file_select = upload_form.find_element(By.CSS_SELECTOR, "input[type=file]")
            file_select.send_keys(os.path.join(self.test_dir, "test_meme.jpg"))

            tag_input = upload_form.find_element(By.CSS_SELECTOR, "tags span")
            tag_input.send_keys("test tag")

            upload_button = upload_form.find_element(
                By.CSS_SELECTOR, "input[type=submit]"
            )
            upload_button.click()

            wait = WebDriverWait(self.driver, 10).until(EC.url_changes(upload_path))

            self.assertTrue(wait)

            self.assertTrue(self.pageFlashesContain("Meme Successfully Uploaded!"))

            tag_link = self.driver.find_element(
                By.XPATH, '//*[@id="memes"]/div[1]/div/div/div/a'
            )
            self.assertEqual(tag_link.text, "#test tag")

    def test_view_meme(self):
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, "test meme")

        home_path = self.getFullWebPath("/")
        self.driver.get(home_path)

        meme_details_link = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f".meme a[href='/meme/{meme_id}']")
            )
        )
        meme_details_link.click()

        wait = WebDriverWait(self.driver, 10).until(EC.url_changes(home_path))

        self.assertTrue(wait)

        full_meme_path = self.getFullWebPath(f"/meme/{meme_id}")
        self.assertEqual(self.driver.current_url, full_meme_path)

        image_element = self.driver.find_element(
            By.CSS_SELECTOR, f"img[src='/meme/image/{meme_id}']"
        )
        is_image_loaded = self.driver.execute_script(
            "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0",
            image_element,
        )
        self.assertTrue(is_image_loaded)

    def test_delete_meme(self):
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, "test meme")

        with self.logged_in_context(user_id):
            full_meme_path = self.getFullWebPath(f"/meme/{meme_id}")
            self.driver.get(full_meme_path)

            delete_trigger = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button.link-danger[data-bs-toggle='modal']")
                )
            )

            delete_trigger.click()

            delete_modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "deleteModal"))
            )

            delete_button = delete_modal.find_element(
                By.CSS_SELECTOR, "button[type=submit]"
            )
            delete_button.click()

            wait = WebDriverWait(self.driver, 10).until(EC.url_changes(full_meme_path))

            self.assertTrue(wait)

            home_path = self.getFullWebPath("/")
            self.assertEqual(self.driver.current_url, home_path)

            self.assertTrue(self.pageFlashesContain("Successfully deleted meme!"))
            self.assertRaises(
                NoSuchElementException,
                self.driver.find_element,
                By.CSS_SELECTOR,
                f".meme a[href='/meme/{meme_id}']",
            )

    def test_download_meme(self):
        user_id = self.createTestUser()
        meme_id = self.createTestMeme(user_id, "test meme")

        full_meme_path = self.getFullWebPath(f"/meme/{meme_id}")
        self.driver.get(full_meme_path)

        meme_filename = f"meme_{meme_id}.jpg"

        download_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"a[download='{meme_filename}']")
            )
        )
        download_button.click()

        time.sleep(0.2)
        file_path = os.path.join(self.download_dir, meme_filename)
        self.assertTrue(os.path.exists(file_path))
