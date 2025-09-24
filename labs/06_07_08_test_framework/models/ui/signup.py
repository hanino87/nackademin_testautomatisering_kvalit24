# Page where the users could either create a new user or
# navigate to Home
class SignupPage:
    def __init__(self, page):
        self.page = page
        #page_(element-type)_(descriptive-name)
        self.signup_input_username = page.get_by_placeholder('Username')
        self.signup_input_password = page.get_by_placeholder('Password')
        self.signup_btn_signup = page.locator('button.button-primary')
        self.signup_btn_login = page.locator('button.btn-blue')


    def signup(self,username,password):
        """" Metod to singup a user  """ 
        self.signup_input_username.fill(username)
        self.signup_input_password.fill(password)
        self.signup_btn_signup.click()
        
    def go_to_home(self):
        """ Metod to navigate to homepage""" 
        self.signup_btn_login.click()