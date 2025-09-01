class HomePage:
    
# -- Locators on HomePage -- # 

    def __init__(self, page):
        self.page = page
        self.product_name_input=page.locator('input[placeholder="Product Name"]')
        self.create_product_button=page.locator('button:has-text("Create Product")')
        self.product_lists=page.locator('.product-grid')

       
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