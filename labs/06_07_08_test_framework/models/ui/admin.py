# View  where the admin user can manage the products
# that are in the Product Catalog to be used
# by all the users


class AdminPage:
    def __init__(self, page):
        self.page = page
        self.login_welcome_message = page.get_by_text('Welcome, admin!')
        self.product_name_input = page.get_by_placeholder('Product Name')
        self.create_product_btn=page.get_by_role("button", name="Create Product")
        self.product_lists=page.locator(".product-grid")
        #page_(element-type)_(descriptive-name)
        #complete admin view elements
   
    def get_current_product_count(self,):
        "Metod for get and count number of products in the product list"
        self.product_lists.wait_for(state="visible")  # wait for the element to be visible to make test more robust 
        grid_items = self.product_lists.locator(".product-item") # assign the products inside the dive 
        count = grid_items.count() 
        return count
        # complete logic
        # return number of total products displayed

    def create_product(self,product_name):
        "Metod for create a product and fill in product name"
        self.product_name_input.wait_for(state="visible")# wait for the element to be visible to make test more robust 
        self.create_product_btn.fill(product_name)
        self.create_product_btn.click()
    
    def create_two_products(self,product_name):
        "Metod for create a product and fill in product name"
        self.product_name_input.wait_for(state="visible")# wait for the element to be visible to make test more robust 
        self.create_product_btn.fill(product_name)
        self.create_product_btn.click()
        self.create_product_btn.fill(product_name)
        self.create_product_btn.click()
  
  

    def delete_product_by_name(self,product_name):
          # Find all products matching the name by go to locators under the paraent product_list use has-text attribute on the product element 
        products = self.product_lists.locator(
            f".product-item:has-text('{product_name}')") 
        
        # Check if any exist
        if products.count() == 0:
            return  # Nothing to delete
        
        # Variable of last product by name in the element .product-item by name not only the last product from the index 
        last_product = products.last 
        
        # Wait for it to be visible
        last_product.wait_for(state="visible")
        
        # Find the Delete button inside the last product product.item 
        delete_btn = last_product.locator(".product-item-button") 
        delete_btn.wait_for(state="visible")

        # Click to delete
        delete_btn.click()

        # Short pause to let DOM update
        self.page.wait_for_timeout(200)
