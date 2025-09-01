import re
from playwright.sync_api import sync_playwright, Page, expect

APP_URL = 'http://localhost:5173'


def test_create_new_user_and_add_and_delete_a_product():
    """
    Full end-to-end test with Playwright:
    1. Open the app
    2. Sign up a new user
    3. Log in with the user
    4. Create a product
    5. Verify that the product appears in the list
    6. Delete the product
    7. Verify deletion
    """

    username = "testuserhannes"
    password = "testpassword"
    product = "Bajen Halsduk"
    non_existing_product = "Aik Tröja"

    # Dialog handler for alerts
    def handle_dialog(dialog):
        dialog.accept()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page: Page = context.new_page()

        # --- Step 1: Open the app ---
        page.goto(APP_URL)

        # --- Step 2: Navigate to signup ---
        signup_nav_button = page.locator("#signup")  # ID locator
        signup_nav_button.click()

        # --- Step 3: Fill in signup form ---
        signup_username_input = page.locator( '//input[@placeholder="Username"]')  # XPath locator
        signup_password_input = page.locator('//input[@placeholder="Password"]')  # XPath locator
        signup_username_input.fill(username)
        signup_password_input.fill(password)

        signup_submit_button = page.locator('.button-primary')  # class selector

        page.once("dialog", handle_dialog)
        signup_submit_button.click()

        # --- Step 4: Log in ---
        login_nav_button = page.locator('.btn-blue')  # class selector
        login_nav_button.click()

        login_username_input = page.locator('//input[@placeholder="Username"]')  # XPath locator
        login_password_input = page.locator('//input[@placeholder="Password"]')  # XPath locator
        login_username_input.fill(username)
        login_password_input.fill(password)

        login_submit_button = page.locator('button:has-text("Login")')  # text selector
        expect(login_submit_button).to_be_enabled()
        expect(login_submit_button).to_be_visible()
        login_submit_button.click()

        # --- Step 5: Create a product ---
        product_name_input = page.locator('input[placeholder="Product Name"]')  # CSS attribute selector
        expect(product_name_input).to_be_visible()
        product_name_input.fill(product)

        create_product_button = page.locator('button:has-text("Create Product")')  # text selector
        expect(create_product_button).to_be_visible()
        expect(create_product_button).not_to_be_hidden()
        create_product_button.click()

        # --- Step 6: Verify the product appears in the list ---
        product_list_container = page.locator( ".product-grid")  # class selector
        expect(product_list_container).to_be_visible()
        expect(product_list_container).to_have_text(re.compile(product))
        expect(product_list_container).not_to_have_text(re.compile(non_existing_product))

        print("✅ Product added successfully!")

        page.wait_for_timeout(5000)  # optional pause

        # --- Step 7: Delete only the last product with this name ---
        product_items = product_list_container.locator(f".product-item:has-text('{product}')")
        count_before = product_items.count()

        # click the delete button inside the last product
        delete_button = product_items.last.locator(".product-item-button") # class selector 
        delete_button.click()

        print(f"✅ Last product named '{product}' deleted successfully!")

        # --- Step 8: Verify deletion ---
        # Verify last product is gone 
        expect(product_items).to_have_count(count_before - 1)

       


