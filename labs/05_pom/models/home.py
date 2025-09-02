class HomePage:
    # --- Locators on Homepage with Semantic Style ---
    def __init__(self, page):
        self.page = page
        # Semantic locators (resilient against CSS/class changes)
        self.product_name_input = page.get_by_placeholder("Product Name")
        self.create_product_btn = page.get_by_role("button", name="Create Product")
        self.product_lists = page.locator(".product-grid")
        self.logout_btn= page.get_by_role("button", name="Logout")

    # --- Page Actions ---
    def navigate(self):
        """Go to the homepage"""
        self.page.goto("http://localhost:5173/")

    def add_product(self,product_titel:str):
        "Metod for create a product and fill " 
        self.product_name_input.fill(product_titel)
        self.create_product_btn.click()
    
    def delete_product_by_name(self,product_title:str):
        "Metod for deleting product by name"
        # Find the product in the product grid
        product_item_in_product_list_by_name = self.product_lists.locator(f"text={product_title}")
        # Assign the button here and not in init beacuase its dynamic element not static element 
        del_btn=product_item_in_product_list_by_name.get_by_role("button", name="Delete")
        del_btn.click()
    
    def delete_product_by_name_for_product_with_duplicate_name(self, product_title: str):
         """Method for deleting all products by name, even if duplicates exist"""
    
        # Get all product items containing the given title
         matching_products = self.product_lists.locator(f"text={product_title}")
    
        # Count how many matches exist
         count = matching_products.count()
    
        # Loop from last to first to avoid skipping items when dom structure updates that why we used reversed risk that it skips element if you go forward 
         for i in reversed(range(count)): # count like index 2 1 0 for reversed 
           product = matching_products.nth(i)  # store the specific product element
           delete_btn = product.get_by_role("button", name="Delete")  # find delete button inside that product that you assign to variable above 
           delete_btn.click() # No self in front of delete_btn beacuse that element is dynamic and oustside init metod 
           

    def logout_from_store(self):
        self.logout_btn.click()
        
         
        
        















    def create_product(self, name: str):
        """Create a new product and return locator of the last added product"""
        self.product_name_input.fill(name)
        self.create_product_button.click()
        return self.product_lists.locator(f".product-item:has-text('{name}')").last

    def get_first_product(self):
        """Return locator for the first product in the grid"""
        return self.product_lists.locator(".product-item").first

    def get_last_product(self):
        """Return locator for the last product in the grid"""
        return self.product_lists.locator(".product-item").last

    def delete_product(self, product_locator):
        """Delete a specific product using its locator"""
        delete_button = product_locator.locator(".product-item-button")
        delete_button.click()

    def delete_first_product(self):
        """Delete the first product in the list"""
        first_product = self.get_first_product()
        self.delete_product(first_product)

    def delete_last_product(self):
        """Delete the last product in the list"""
        last_product = self.get_last_product()
        self.delete_product(last_product)
