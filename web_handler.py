""" Handles actions on Pencil's website """

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from webdriver_manager.chrome import ChromeDriverManager

import pyautogui


class PencilHandler:


    def __init__(self, log: object) -> None:
        self.driver_path  =  ChromeDriverManager().install()
        self.driver = Chrome()
        self.log = log

    def open_website(self, url: str):

        try:
            self.driver.get(url)
            self.driver.maximize_window()
            sleep(2)
        except Exception as error:
            self.log.register_error("Exception ocurred when opening page: %s" % error)
            raise error
        
    def login(self, user: str, password: str) -> str:

        try:
            entry_field = 'app-pencil-button.pencil-button:nth-child(2) > button:nth-child(1)'
            wait = WebDriverWait(self.driver, 10)
            item = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, entry_field)))
            item.click()

            sleep(2)
            email_field = self.driver.find_element(By.XPATH, '//*[@id="email-value"]')
            email_field.click()
            email_field.send_keys(user)

            continue_btn = self.driver.find_element(By.XPATH, '//*[@id="emailInputContinue"]/button')
            continue_btn.click()
            sleep(2)
            

            pwd_field_xpath =  '//*[@id="password-value"]'
            pwd_field = wait.until(EC.visibility_of_element_located((By.XPATH, pwd_field_xpath)))
            pwd_field.click()
            pwd_field.send_keys(password)
            enter_button = self.driver.find_element(By.XPATH,'//*[@id="emailPasswordContinue"]/button')
            enter_button.click()

            message = "Login was made successfully!"
            
        except Exception as error:
            self.log.register_error("Exception ocurred while loging into system: %s" % error)
            message = "Could not finish login process. Check the logs for error."

        finally:
            return message
        

    def check_load_time(self) -> bool:
        try:
            self.driver.implicitly_wait(1)
            spaces_table = self.driver.find_element(By.TAG_NAME, 'tbody')
            if spaces_table:
                loaded = True
        except Exception as error:
            message = "could not load item properly. Error -->> %s" % error
            self.log.register_error(message)
            loaded = False

        finally:
            return loaded
        

    def validate_home_format(self) ->  dict:
        try:
            sleep(5)
            results = {}
            spaces_table = self.driver.find_element(By.TAG_NAME, 'tbody')
            rows = spaces_table.find_elements(By.TAG_NAME, 'tr')
            amount = len(rows) - 1

            results['Existing Space'] = amount

            # Check space title
            space_title = rows[0].text
            space = space_title.strip()
            if "My First Space" in space:
                print("Space exists")
                space = 'My First Space'
            
            results['First Space'] = space


            # Check navigation panel

            navigation_panel = self.driver.find_element(By.XPATH, '/html/body/app-root/section/div/div[1]/div[2]/div/ui-nav-bar/div/div[1]')
            fields = navigation_panel.find_elements(By.TAG_NAME, 'li')
            first_opt = fields[0].get_property('innerText')
            second_opt = fields[1].get_property('innerText')

            navigation_options = [first_opt,second_opt]

            requested_options = ['Home', 'Messages']

            if navigation_options == requested_options:
                print('Options are available')
                navigation_options = True
            else:
                navigation_options = False
            
            results['Options'] = navigation_options

            # Check 'create space' button exists:
            functional_button = self.driver.find_element(By.XPATH,'//*[@id="active-session"]/div/app-spaces-view/div/app-spaces-header/ui-header/div[2]/div/app-pencil-button[2]/button')
            button_name = functional_button.get_property('innerText').strip()

            if 'Create Space' in button_name:
                print('Create space button exists')
                results['Create Space'] = True
            else:
                results['Create Space'] = False

            # Check profile pic available:
            profile_field = self.driver.find_element(By.CSS_SELECTOR,'app-profile-photo.cursor-pointer > div:nth-child(1) > app-lightweight-user-avatar:nth-child(1) > div:nth-child(1) > div:nth-child(1) > img:nth-child(1)')
            image = profile_field.get_property('src')

            if image != '':
                results['Image Available'] = True
            else:
                results['Image Available'] = False

        except Exception as error:
            self.log.register_error(error)
        
        finally:
            return results
        

    def enter_first_space(self) -> bool:
        try:
            spaces_table = self.driver.find_element(By.TAG_NAME, 'tbody')
            workspace = spaces_table.find_elements(By.TAG_NAME, 'tr')
            workspace[0].click()
            sleep(2)
            enter_space = self.driver.find_element(By.XPATH,
                '//*[@id="active-session"]/div/app-spaces-view/div/div/app-spaces-details-view/footer/app-pencil-button/button')
            enter_space.click()

            sleep(4)
        except Exception as error:
            self.log.register_error(error)


    def manipulate_canvas(self) -> str:
        try:

            activate_pencil = self.driver.find_element(By.XPATH,'//*[@id="space-toolbar-container"]/app-space-toolbar-holder/div/div/div[4]/div/app-space-toolbar-button/div/div/div/button/span[1]/div/div')
            activate_pencil.click()

            canvas = self.driver.find_element(By.XPATH,'//*[@id="app-wb-canvas"]/div/canvas[2]')

            start_x, start_y = 50, 50
            end_y = 100
            
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, start_x, start_y).click_and_hold()
            actions.move_by_offset(0, end_y).release().perform()

            sleep(2)

            start_x, start_y = 50, 80
            pointer = self.driver.find_element(By.CSS_SELECTOR, '#space-toolbar-container > app-space-toolbar-holder > div > div > div:nth-child(1) > div > app-space-toolbar-button > div > div > div > button > span.mat-button-wrapper > div')
            pointer.click()
            sleep(2)

            # Move item to the right, 10 PX
            actions.move_to_element_with_offset(canvas, start_x, start_y).click_and_hold()
            actions.move_by_offset(60,0).release().perform()

            # Write on text box:

            text_box_btn = self.driver.find_element(By.CSS_SELECTOR, '#space-toolbar-container > app-space-toolbar-holder > div > div > div:nth-child(7) > div > app-space-toolbar-button > div > div > div > button > span.mat-button-wrapper > div')
            text_box_btn.click()
            sleep(1)
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, 100, 150).click_and_hold()
            actions.move_by_offset(60,0).release().perform()
            sleep(5)
            pyautogui.typewrite("this is a test")

            # click outside box
            sleep(6)
            pyautogui.click(900,300)

            message = 'Action to draw, move line and write was executed successfully.'
        except Exception as error:
            self.log.register_error(error)
            message = f"Error occured ->> {error}"

        finally:
            return message
        

    def bonus_assignment(self):
        try:
            sleep(8)
            new_space_btn = self.driver.find_element(By.XPATH,'//*[@id="active-session"]/div/app-spaces-view/div/app-spaces-header/ui-header/div[2]/div/app-pencil-button[2]/button')
            new_space_btn.click()

            sleep(8)
            text_box_btn = self.driver.find_element(By.CSS_SELECTOR, '#space-toolbar-container > app-space-toolbar-holder > div > div > div:nth-child(7) > div > app-space-toolbar-button > div > div > div > button > span.mat-button-wrapper > div')
            text_box_btn.click()
            sleep(5)

            # move mouse to activate text box
            canvas = self.driver.find_element(By.XPATH,'//*[@id="app-wb-canvas"]/div/canvas[2]')
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(canvas, 100, 150).click_and_hold()
            actions.move_by_offset(60,0).release().perform()
            
            # write
            sleep(3)
            pyautogui.typewrite("test")
            sleep(2)
            pyautogui.hotkey('ctrl', 'a')
            sleep(2)

            # Italicize text
            italic_btn = self.driver.find_element(By.CSS_SELECTOR, '#app-wb-canvas > app-fabric-context-menu > app-wrapper-widget > div > div > app-space-toolbar-holder > div > app-space-toolbar-button:nth-child(2) > div > div > div > button')
            italic_btn.click()

            # CLick outside box
            sleep(2)
            pyautogui.click(900,300)
            sleep(1)
            
            bonus_actions_completed =  True

        except Exception as error:
            self.log.register_error(error)
            bonus_actions_completed = False
            
        finally:
            return bonus_actions_completed


    def logout(self) -> bool:
        try:
            space_info = self.driver.find_element(By.XPATH,'//*[@id="top-bar-left-section"]/div[1]/app-space-icon')
            space_info.click()
            options_table = self.driver.find_element(By.XPATH, '//*[@id="mat-menu-panel-27"]/div')
            options = options_table.find_elements(By.TAG_NAME, 'button')

            sleep(1)
            options[0].click()
            sleep(3)
            user_icon = self.driver.find_element(By.XPATH, '//*[@id="btn-home-avatar-menu"]')
            user_icon.click()
            sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, '#mat-menu-panel-43 > div')
            fields = self.driver.find_element(By.CSS_SELECTOR, '#mat-menu-panel-43 > div')
            sign_out_btn = fields.find_elements(By.TAG_NAME, 'button')[2]
            sign_out_btn.click()
            confirm_option = self.driver.find_element(By.CSS_SELECTOR, '#mat-dialog-0 > app-logout-dialog > div > app-pencil-button.pencil-button.btn-primary.flex-1.cml-16 > button')
            confirm_option.click()

            # Check if login page is returned:
            entry_field = 'app-pencil-button.pencil-button:nth-child(2) > button:nth-child(1)'
            wait = WebDriverWait(self.driver, 10)
            item = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, entry_field)))

            if item:
                return True
            else:
                return False
            
        except Exception as error:
            self.log.register_error(error)
            return False

        finally:
            #  close Browser
            self.driver.quit()

