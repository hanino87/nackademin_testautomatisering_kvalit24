from playwright.sync_api import Page, expect
from test.test_config import login_as_admin

# -------------------------------------------------------
# Admin E2E tests 
# -------------------------------------------------------
  
def test_add_product_to_catalog(page: Page):
    """Verify that admin can add a product"""
    home_page, admin_page = login_as_admin(page)
    admin_page.create_product("fish")

    fish_locator = admin_page.page.locator(".product-grid span", has_text="fish")
    expect(fish_locator).to_be_visible()

    total_products = len(admin_page.get_current_product_count())
    assert total_products == 2, f"Expected 2 products, got {total_products}"
    print("✅ Product added. Total products:", total_products)

def test_remove_product_from_catalog(page: Page):
    """Verify that admin can remove a product"""
    home_page, admin_page = login_as_admin(page)
    admin_page.delete_product_by_name("fish")

    fish_locator = admin_page.page.locator(".product-grid span", has_text="fish")
    expect(fish_locator).to_be_hidden()

    total_products = len(admin_page.get_current_product_count())
    assert total_products == 1, f"Expected 1 product, got {total_products}"
    
    empty_basket_message = admin_page.no_products_header_text
    expect(empty_basket_message).to_be_hidden()
    if empty_basket_message.is_hidden():
        print("✅ Product is gone. Total products: 1")
    else:
        print("❌ Empty basket message visible unexpectedly.")

