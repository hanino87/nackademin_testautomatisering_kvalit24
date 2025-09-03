class ProductPage:
    def __init__(self, page):
        self.page = page
        # Semantic locators (robust against style/DOM changes)
        self.product_name_input = page.get_by_placeholder("Product Name")
        self.create_product_btn = page.get_by_role(
         "button", name="Create Product")
        self.product_lists = page.locator(".product-grid")
        self.logout_btn = page.get_by_role("button", name="Logout")
        self.empty_product_message = page.get_by_text("No products available.")
        
        # --- Page Actions ---
    def navigate(self):
        """Go to the homepage"""
        self.page.goto("http://localhost:5173/")

    def add_product(self, product_titel: str):
        "Metod for create a product and fill in product name"
        self.product_name_input.wait_for(state="visible")
        self.product_name_input.fill(product_titel)
        self.create_product_btn.click()

    def delete_product_by_name(self, product_title: str):
        """Delete the last occurrence of a product by name"""

        # Find all products matching the name
        products = self.product_lists.locator(
            f".product-item:has-text('{product_title}')")
        
        # Check if any exist
        if products.count() == 0:
            return  # Nothing to delete
        
        # Get the last product
        last_product = products.last
        
        # Wait for it to be visible
        last_product.wait_for(state="visible")
        
        # Find the Delete button inside the last product
        delete_btn = last_product.locator(".product-item-button")
        delete_btn.wait_for(state="visible")

        # Click to delete
        delete_btn.click()

        # Short pause to let DOM update
        self.page.wait_for_timeout(200)
       
    def delete_all_products_in_store(self):
        """delete all products in the list"""
        product_grid=self.product_lists
        items= product_grid.locator(".product-item")
        delete_btn_selector= ".product-item-button"
        
        total_items=items.count()
        
        for _ in range(total_items): 
            items.first.locator(delete_btn_selector).click()
    
    def logout_from_store(self):
        """logout from store as a perfect teardown in each test"""
        self.logout_btn.click()
       
       
  
    
    
