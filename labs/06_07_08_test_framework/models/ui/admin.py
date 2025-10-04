# Page  where the admin user can manage the products
# that are in the Product Catalog to be used
# by all the users
from libs.config import get_frontend_url

class AdminPage:
    def __init__(self, page):
        self.page = page
        self.base_url = get_frontend_url() 
        self.product_name_input = page.locator('input[placeholder="Product Name"]')
        self.create_product_btn=page.get_by_role("button", name="Create Product")
        self.welcome_message = page.locator("h2:has-text('Welcome')")
        self.products_header_text=page.locator("h3:has-text('Products available:')")
        self.no_products_header_text=page.locator("p:has-text('No products available.')")
        self.product_grid=page.locator(".product-grid")
        self.product_list=page.locator(".product-grid > .product-item > span") # go down in the domstructur to product items span elment which contains productname 
        self.logout_btn=page.get_by_role("button", name="Logout")
       
        #page_(element-type)_(descriptive-name)
        #complete admin view elements
    
    def navigate(self):
        """Go to admin page safely using base_url."""
        if not self.base_url:
            raise ValueError("Frontend URL is missing! Check test_config.py or environment variables.")
        self.page.goto(self.base_url)
   
    def get_current_product_count(self):
      """Get and return all product names as a list"""
    # Wait for the grid or at least one product to be visible
      self.product_list.first.wait_for(state="visible", timeout=5000)
      # Return list of product names
      return [p.inner_text().strip() for p in self.product_list.all()]
  
    
    def create_product(self,product_name:str):
        """Metod for create a product and fill in product name"""
        self.product_name_input.wait_for(state="attached")
        self.product_name_input.fill(product_name)
        self.create_product_btn.click()
        self.page.locator(".product-grid > .product-item > span", has_text=product_name).wait_for(state="visible")
    
    
    def delete_product_by_name(self, product_name:str):
        """ Metod to delete product by name"""
        product_div = self.page.locator(
            f'//div[@class="product-item"][span[text()="{product_name}"]]' # nicer xapth to find the element 
        )
        product_div.locator("button.product-item-button").click() # in the grid find button with class product-item-button 

        
    def delete_all_products_in_store(self):
        """Metod delete all products in the list"""
        product_grid=self.product_lists
        items= product_grid.locator(".product-item")
        delete_btn_selector= ".product-item-button"
        
        total_items=items.count()
        
        for _ in range(total_items): 
            items.first.locator(delete_btn_selector).click()
    
    def logout_from_store(self):
        """Metod logout from store as a perfect teardown in each test"""
        self.logout_btn.click()