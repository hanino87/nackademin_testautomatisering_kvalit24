# Landing page where the users could either login or
# navigate to signup
import libs.utils
import os 
from dotenv import load_dotenv

# Load .env once at the top of the test file
load_dotenv()

class HomePage:
    def __init__(self, page):
        self.page = page
        #page_(element-type)_(descriptive-name)
        self.login_header_main_title = page.get_by_text('Nackademin Course App')
        self.login_input_username = page.get_by_placeholder('Username')
        self.login_input_password = page.get_by_placeholder('Password')
        self.login_btn_login = page.locator('button.button-primary')
        self.login_label_have_account = page.get_by_text("Don't have an account?")
        self.login_btn_signup = page.locator('#signup')
        self.base_url = os.getenv("BASE_URL_FRONTEND")

    def navigate(self):
        self.page.goto(self.base_url)


    def login(self,username,password):
        self.login_input_username.fill(username)
        self.login_input_password.fill(password)
        self.login_btn_login.click()

    def go_to_signup(self):
        self.login_btn_signup.click()