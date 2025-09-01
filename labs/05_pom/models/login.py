# Implement PO for login
# 2 inputs and 1 button
# Naming example:  input_username

class LoginPage:
    
# -- Locators on LoginPage -- # 
    def __init__(self, page):
        self.page = page
        self.login_input_username = page.locator(('//input[@placeholder="Username"]'))
        self.login_input_password = page.locator(('//input[@placeholder="Password "]'))
        self.button_login = page.locator('.button-primary')
        self.button_signup = page.locator("#signup")
        
# -- Actions on LoginPage -- # 
    def navigate_to_signup(self):
        self.button_signup.click()
    
    
    # Login a registered user 
    def register_user(self, username: str, password: str):
        self.login_input_password.fill(password)
        self.login_input_username.fill(username)
        self.button_login.click()

    