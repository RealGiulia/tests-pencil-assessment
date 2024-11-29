import unittest
from logger import Logger
from user_input import INPUT_READER
from web_handler import PencilHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPencilHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = INPUT_READER()
        cls.email = config.parser('EMAIL')
        cls.pwd = config.parser('SECRET')
        cls.log_path = config.parser("LOG_FOLDER")

        cls.log = Logger(cls.log_path)
        cls.web = PencilHandler(cls.log)
        cls.web.open_website('https://my.pencilapp.com/account/login')

    def test_01_login(self):
        # Log in
        login_status = self.web.login(self.email, self.pwd)
        self.assertIn("Login was made successfully!", login_status, "Login failed")

    def test_bonus_assignment(self):
        # Perform bonus assignment actions
        bonus_completed = self.web.bonus_assignment()
        self.assertTrue(bonus_completed, "Bonus assignment actions failed")

    @classmethod
    def tearDownClass(cls):
        cls.web.driver.quit()

if __name__ == "__main__":
    unittest.main()


