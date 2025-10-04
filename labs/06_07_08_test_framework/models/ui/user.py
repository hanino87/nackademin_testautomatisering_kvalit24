# Page where an user (non admin) can see their user products 

class UserPage:
    def __init__(self, page,username,):
        self.page = page
        self.header_title = page.get_by_text("Nackademin Course App")
        self.welcome_message_with_username = page.get_by_text(f"Welcome, {username}", exact=False) # false to make if work in 
        self.user_header_products_title_with_products = page.get_by_text("Your Products:") # but this is dangerous if there are same texts on the page somewhere 
        self.user_header_products_title_with_products = page.get_by_text("No products assigned.") # but this is dangerous if there are same texts on the page somewhere 
        self.btn_logout = page.get_by_role("button", name="Logout")
        self.grid_locator = page.locator("#root > div > div")
        self.btn_add_product = page.get_by_role("button", name="Add Product")
        self.txt_product=page.get_by_text("Your Products:")
        self.btn_add_in_popup_window=page.get_by_role("button", name="Add", exact=True)
        self.btn_close=page.get_by_role("button", name="Close")
        self.txt_no_products=page.get_by_text("No more products available.")
        self.btn_delete=page.get_by_role("button", name="Delete")
        self.customers_product_list=page.locator("#root div div div div") #has_text="Laptop")
        #page_(element-type)_(descriptive-name)
       
    def get_user_products(self):
        """"Metod to get user products"""
        
        # potential grid on webpage thats why its not in the instructor beacuse init is for element that is static on the webpage 
        grid_with_products=self.page.locator("#root > div > div") # took id root and then go down 2 step in dom element to find the grid with products 
        
         # Check if user has no products assigned by going down to p element in the last grid 
        if self.grid_locator.locator("p", has_text="No products assigned.").is_visible():
            return []
        
        # check if user has product and if so list them # here you go down to check all div in the product grid and each represent an product 
        product_divs = grid_with_products.locator("div") 
        
        # get all texts from the grids 
          
        product_texts = [div.inner_text() for div in product_divs.all()] # assing all inner text from every produt-item grid from the whole grid of products 
        return product_texts # return it as a whole list 
    
    def logout(self):
        """"Metod to logout from userpage"""
        self.button_logout.click()
        

    def add_product_to_user(self): # Misses in frontend ui-mode 
        self.btn_add_product.click()
        self.btn_add_in_popup_window.click()
        self.btn_close.click()
        

    def remove_product_from_user(self):# Misses in frontend ui-mode 
        self.btn_delete.click()