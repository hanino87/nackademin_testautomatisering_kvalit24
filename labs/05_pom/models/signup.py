class SignupPage:
    def __init__(self, page):
        self.page = page
        # Semantic locators (robust and easier to read)
        self.signup_input_username = page.get_by_placeholder("Username")
        self.signup_input_password = page.get_by_placeholder("Password")
        self.signup_submit_btn = page.get_by_role("button", name="Sign Up")  
        # ⚠️ Adjust "Sign Up" to match the actual button text in your app

    # --- Actions on Signup page --- #
    def register_user(self, username: str, password: str):
        """Fill in signup form and submit"""
        self.signup_input_username.fill(username)
        self.signup_input_password.fill(password)
        self.signup_submit_btn.click()

    def handle_dialog(self, dialog):
        """Handle confirmation/alert dialogs during signup"""
        dialog.accept()
