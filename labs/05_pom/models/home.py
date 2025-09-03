class HomePage:
    # --- Locators on Homepage with Semantic Style ---
    def __init__(self, page):
        self.page = page
        

    # --- Page Actions ---
    def navigate(self):
        """Go to the homepage"""
        self.page.goto("http://localhost:5173/")

