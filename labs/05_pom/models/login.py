# Implement PO for login
# 2 inputs and 1 button
# Naming example:  input_username

class LoginPage:
    
# -- Locators on LoginPage without Semantic Style with CSS & XPath Style  -- # 
    def __init__(self, page):
        self.page = page
        self.login_input_username = page.locator(('//input[@placeholder="Username"]'))
        self.login_input_password = page.locator(('//input[@placeholder="Password "]'))
        self.button_login = page.locator('.button-primary')
        self.button_signup = page.locator("#signup")


# -- Locators on LoginPage with Semantic Style -- #

    def __init__(self, page):
        self.page = page
        # replaces //input[@placeholder="Username"]
        self.login_input_username = page.get_by_placeholder("Username")
        # replaces //input[@placeholder="Password "]
        self.login_input_password = page.get_by_placeholder("Password")
        # replaces .button-primary (assuming the button text is "Login")
        self.button_login = page.get_by_role("button", name="Login")
        # replaces #signup
        self.button_signup = page.get_by_role("link", name="Sign Up")  # if it's a link
        # OR
        # self.button_signup = page.get_by_role("button", name="Sign Up")  # if it's a button

# -- Actions on LoginPage -- # 
    def navigate_to_signup(self):
        self.button_signup.click()
    
    
    # Login a registered user 
    def register_user(self, username: str, password: str):
        self.login_input_password.fill(password)
        self.login_input_username.fill(username)
        self.button_login.click()

    