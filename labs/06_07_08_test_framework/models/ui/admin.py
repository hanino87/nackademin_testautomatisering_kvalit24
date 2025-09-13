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
        grid_items = self.product_lists.locator(".product-item")
        count = grid_items.count() 
        return count
        # complete logic
        # return number of total products displayed

    def create_product(self,product_name):
        self.create_product_btn.fill(product_name)
        
        
        # complete logic

    def delete_product_by_name(self,product_name):
        # complete logic
