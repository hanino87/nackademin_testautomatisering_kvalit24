# Implement PO for signup
# 2 inputs and 1 button
# Naming example:  signup_input_username
class SignupPage:

# -- Locators on LoginPage without Semantic Style with CSS & XPath Style  -- # 

    def __init__(self, page):
        self.page = page
        self.singup_input_username = page.locator(('//input[@placeholder="Username"]'))
        self.signup_input_password= page.locator(('//input[@placeholder="Password"]'))
        self.signup_submit_button = page.locator('.button-primary') 
        #self.button_login = page.locator(??)
    
# -- Locators on Homepage with Semantic Style  Makes the locators more robust in testing --

    def __init__(self, page):
        self.page = page
        # Instead of XPath with placeholder:
        self.signup_input_username = page.get_by_placeholder("Username")
        self.signup_input_password = page.get_by_placeholder("Password")
        # Instead of class selector for primary button:
        self.signup_submit_button = page.get_by_role("button", name="Sign Up")  
         # (⚠️ Adjust "Sign Up" to match the actual button text in your app)
       
# -- Actions on Signup page -- # 
    
     # Fill in all user details 
    def register_user(self, username: str, password: str):
        self.signup_input_password.fill(password)
        self.singup_input_username.fill(username)
        self.signup_submit_button.click()
        
    # Dialog handler for alerts
    def handle_dialog(dialog):
        dialog.accept()