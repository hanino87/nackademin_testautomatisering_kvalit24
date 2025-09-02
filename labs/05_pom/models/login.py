class LoginPage:
    # --- Locators on LoginPage with Semantic Style ---
    def __init__(self, page):
        self.page = page
        # Semantic locators (robust against style/DOM changes)
        self.login_input_username = page.get_by_placeholder("Username")
        self.login_input_password = page.get_by_placeholder("Password")
        self.btn_login = page.get_by_role("button", name="Login")
        self.btn_signup = page.locator("#signup")
        # If "Sign Up" is actually a button in your app:
        # self.button_signup = page.get_by_role("button", name="Sign Up")

    # --- Actions on LoginPage ---
    def navigate_to_signup(self):
        """Click the Sign Up button/link to navigate to signup page"""
        self.btn_signup.click()

    def login_with_user_that_exist_in_database(self, username: str, password: str):
        """Log in as an existing user"""
        self.login_input_username.wait_for(state="visible")
        self.login_input_username.fill(username)
        self.login_input_password.fill(password)
        self.btn_login.click()
    
    def login_with_no_user_info(self, bad_username: str, bad_password: str):
        """Log in as an non existing user"""
        self.login_input_username.fill(bad_username)
        self.login_input_password.fill(bad_password)
        self.btn_login.click()
    
    def login_with_user_that_dont_exist_in_database(self, bad_username: str, bad_password: str):
        """Log in as an non existing user"""
        self.login_input_username.fill(bad_username)
        self.login_input_password.fill(bad_password)
        self.btn_login.click()
    
    

