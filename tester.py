"""FIle to apply tests on Pencil App webpage."""

import unittest
from logger import Logger
from user_input import INPUT_READER
from web_handler import PencilHandler


class TestPencilHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config = INPUT_READER()
        cls.email = config.parser('EMAIL')
        cls.pwd = config.parser('SECRET')
        cls.log_path = config.parser("LOG_FOLDER")

        cls.log = Logger(cls.log_path)
        cls.web = PencilHandler(cls.log)
        cls.web_secondary = PencilHandler(cls.log)


    def test_01_login(self):
        # Open website and login
        url = 'https://my.pencilapp.com/account/login'
        self.web.open_website(url)
        login_status = self.web.login(self.email, self.pwd)
        self.assertIn("Login was made successfully!", login_status, "Login failed")


    def test_02_check_load_time(self):
        # Check the load time
        loaded = self.web.check_load_time()
        self.assertTrue(loaded, "Page has taken longer to load")


    def test_03_validate_home_format(self):
        # Validate the home format
        formats = self.web.validate_home_format()
        self.assertGreaterEqual(formats.get('Existing Space', 0), 0)
        self.assertEqual(formats['First Space'], "My First Space", "Space title is not 'My First Space'")
        self.assertTrue(formats['Options'], "Navigation options are different from expected")
        self.assertTrue(formats['Create Space'], "'Create Space' button not available")
        self.assertTrue(formats['Image Available'], "Profile picture avatar is not visible")


    def test_04_enter_first_space(self):
        # Enter the first space
        entered = self.web.enter_first_space()
        self.assertIsNone(entered, "Failed to enter the first space")


    def test_05_manipulate_canvas(self):
        # Manipulate the canvas
        manipulation = self.web.manipulate_canvas()
        self.assertIn("Action to draw, move line and write was executed successfully.", manipulation, "Canvas manipulation failed")


    def test_06_logout_and_redirect(self):
        # Logout and check redirection
        logout = self.web.logout()
        self.assertTrue(logout, "Logout failed")
        
        # Verify redirect from another URL
        new_url = 'https://my.pencilapp.com'
        self.web_secondary.open_website(new_url)
        login_status = self.web_secondary.login(self.email, self.pwd)
        self.assertIn("Login was made successfully!", login_status, "Login after redirection failed")


    @classmethod
    def tearDownClass(cls):
        cls.web_secondary.driver.quit()


if __name__ == "__main__":
    unittest.main()
