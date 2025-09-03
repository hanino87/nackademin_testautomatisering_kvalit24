from playwright.sync_api import Page, expect
from models.home import HomePage
from models.login import LoginPage
from models.signup import SignupPage 

def test_add_product_to_catalog(page: Page):
    
    "Test is done after this Requirments below"
    
    # Given I am an admin user​
    # When I add a product to the catalog​
    # Then The product is available to be used in the app
    
    #POM
    home_page = HomePage(page)
    login_page = LoginPage(page)
    signup_page=SignupPage(page)
    
    home_page.navigate()
    login_page.navigate_to_signup()
    signup_page.register_user("testuser","secret")
    signup_page.page.on("dialog", lambda dialog: signup_page.handle_dialog(dialog))
    home_page.navigate() # go back to page manually you go to inlogpage after signup but in the automation you have to navigate extra step 
    login_page.login_with_user_that_exist_in_database("testuser","secret")
    home_page.add_product("Bajen Shirt")
    home_page.add_product("Fish")
    home_page.add_product("Bajen Shirt")
    
    # Assert the latest added "Bajen Shirt" is visible (duplicate-safe)
    expect(home_page.product_lists.get_by_text("Bajen Shirt").nth(-1)).to_be_visible()
    expect(home_page.product_lists.get_by_text("Bajen Shirt").nth(-1)).not_to_be_hidden()
    
    # Assert that the list dont contain an product i havent "added"
    expect(home_page.product_lists.get_by_text("Computer")).not_to_be_visible()
    expect(home_page.product_lists.get_by_text("Computer")).to_be_hidden()
    
    # Assert that the list contain Fish is visbile (not duplicate product)
    expect(home_page.product_lists.get_by_text("Fish")).to_be_in_viewport()
    
    # Assert list of products is not empty anymore after adding products
    expect(home_page.empty_product_message).not_to_be_in_viewport()
    
    # Teardown    
    home_page.logout_from_store()
   
def test_remove_product_from_catalog(page: Page):
    
    "Test is done after this Requirments below"
    
    # Given I am an admin user​
    # When I remove a product from the catalog​
    # Then The product should not be listed in the app to be used
    
    #POM
    home_page = HomePage(page)
    login_page = LoginPage(page)
    
    home_page.navigate()
    login_page.login_with_user_that_exist_in_database("testuser","secret")
    home_page.delete_product_by_name(("Fish"))
    
    # Assert that the Fish product is gone
    expect(home_page.product_lists.get_by_text("Fish")).to_be_hidden()
    expect(home_page.product_lists).not_to_contain_text("Fish")
    
    # Assert that the other products in the store has not been deleted 
    expect(home_page.product_lists).to_contain_text("Bajen Shirt")
    
    # Assert that by deleting just one product the store is not empty of products
    expect(home_page.empty_product_message).to_be_hidden()
    
    home_page.delete_all_products_in_store()
    
    # Assert that all products in store is gone the product catalog should be empty 
    expect(home_page.empty_product_message).to_be_visible()
    
    # Teardown
    home_page.logout_from_store()
   
    
    