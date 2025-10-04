# Page where the users could either login a new user or
# navigate to Singup 
from playwright.sync_api import Page
from libs.config import get_frontend_url

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = get_frontend_url()  # ensures URL is valid

        # Page elements
        self.login_header_main_title = page.get_by_text('Nackademin Course App')
        self.login_input_username = page.get_by_placeholder('Username')
        self.login_input_password = page.get_by_placeholder('Password')
        self.login_btn_login = page.locator('button.button-primary')
        self.login_label_have_account = page.get_by_text("Don't have an account?")
        self.login_btn_signup = page.locator('#signup')

    def navigate(self):
        """ Metod to navigate to frontend url """
        if not self.base_url:
            raise ValueError("Frontend URL is missing! Check test_config.py or environment variables.")
        self.page.goto(self.base_url)

   
    def login(self, username: str, password: str):
        """Metod to login """
        self.login_input_username.fill(username)
        self.login_input_password.fill(password)
        self.login_btn_login.click()
        
        """" Metod to go to singup page from homepage"""
    def go_to_signup(self):
        self.login_btn_signup.click()
