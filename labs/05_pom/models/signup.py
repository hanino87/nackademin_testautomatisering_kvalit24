# Implement PO for signup
# 2 inputs and 1 button
# Naming example:  signup_input_username



class SignupPage:

# -- Locators on SignupPage -- # 

    def __init__(self, page):
        self.page = page
        self.singup_input_username = page.locator(('//input[@placeholder="Username"]'))
        self.signup_input_password= page.locator(('//input[@placeholder="Password"]'))
        self.signup_submit_button = page.locator('.button-primary') 
        #self.button_login = page.locator(??)
       
# -- Actions on Signup page -- # 
    
     # Fill in all user details 
    def register_user(self, username: str, password: str):
        self.signup_input_password.fill(password)
        self.singup_input_username.fill(username)
        self.signup_submit_button.click()
        
    # Dialog handler for alerts
    def handle_dialog(dialog):
        dialog.accept()