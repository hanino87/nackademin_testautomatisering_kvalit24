class HomePage:
    
# -- Locators on LoginPage without Semantic Style with CSS & XPath Style  -- # 

    def __init__(self, page):
        self.page = page
        self.product_name_input=page.locator('input[placeholder="Product Name"]')
        self.create_product_button=page.locator('button:has-text("Create Product")')
        self.product_lists=page.locator('.product-grid')
    
# -- Locators on Homepage with Semantic Style  Makes the locators more robust in testing --
    def __init__(self, page):
        self.page = page
        # Instead of CSS, use semantic locators
        self.product_name_input = page.get_by_placeholder("Product Name")  # replaces input[placeholder="Product Name"]
        self.create_product_button = page.get_by_role("button", name="Create Product")  # replaces button:has-text("Create Product")
        self.product_lists = page.locator('.product-grid')  # keeping grid by class, but could refine if needed

   
# -- Actions on HomePage -- # 
    def navigate(self):
        self.page.goto("http://localhost:5173/")
    
    
    def create_a_product(self):
        pass 
    
    
    # Create product and return the locator for the newly last added product by name 
    def create_product(self, name: str):
        self.product_name_input.fill(name)
        self.create_product_button.click()
        # Return a locator for the **exact product just added and also the last with that specific name of product **
        return self.product_lists.locator(f".product-item:has-text('{name}')").last # use locator from init metod above 
    
    def get_first_product(self):
        return self.product_lists.locator(".product-item").nth(0)

    def get_last_product(self):
        return self.product_lists.locator(".product-item").last

    # Delete a specific product using its locator
    def delete_product(self, product_locator):
        delete_button = product_locator.locator(".product-item-button")
        delete_button.click()
    
    
    # --- Delete first product --- #
    def delete_first_product(self):
        first_product = self.get_first_product()
        self.delete_product(first_product)

    # --- Delete last product --- #
    def delete_last_product(self):
        last_product = self.get_last_product()
        self.delete_product(last_product)