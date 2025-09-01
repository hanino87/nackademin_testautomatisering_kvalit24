# import re
# from playwright.sync_api import Page, expect


# def test_has_title(page: Page):
#     page.goto("https://playwright.dev/")
#     expect(page).to_have_title(re.compile("Playwright"))
#     expect(page.get_by_text("Get started")).to_be_visible()

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
        signup_username_input = page.locator('//input[@placeholder="Username"]')  # XPath locator
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
        product_list_container = page.locator(".product-grid")  # class selector
        expect(product_list_container).to_be_visible()
        expect(product_list_container).to_have_text(re.compile(product))
        expect(product_list_container).not_to_have_text(re.compile(non_existing_product))

        print("✅ Product added successfully!")

        page.wait_for_timeout(5000)  # optional pause

        # --- Step 7: Delete the product ---
        first_product_item = product_list_container.locator(".product-item").first  # class selector within container
        delete_product_button = first_product_item.locator(".product-item-button")  # class selector within product item
        delete_product_button.click()

        print("✅ Product deleted successfully!")

        # --- Step 8: Verify deletion ---
        deleted_product_locator = page.locator(f".product-grid >> text='{product}'")  # chained class + text locator
        expect(deleted_product_locator).to_have_count(0)

        # --- Teardown ---
        context.close()
        browser.close()



# ### Selenium Code Below 

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By   # ✅ Better way to locate elements
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # The URL where your frontend app is running
# APP_URL = 'http://localhost:5173'

# # Setup Chrome options (disable unnecessary logs)
# options = Options()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])


# def test_create_new_user():
#     """
#     Full end-to-end test:
#     1. Open the app
#     2. Sign up a new user
#     3. Log in with that user
#     4. Create a product
#     5. Verify the product is visible in the list
#     """
    
#     username = "testuserhannes"
#     password = "testpassword"
#     product = "Bajen Halsduk"  # Product name we want to create
#     non_existing_product="Aik Tröja"

#     # --- Arrange / Setup ---
#     driver = webdriver.Chrome(options=options)
#     driver.get(APP_URL)  # Open the app in the browser

#     # --- Step 1: Navigate to Signup form ---
#     signup_btn = driver.find_element(By.ID, "signup")
#     signup_btn.click()

#     # --- Step 2: Fill in signup form ---
#     signup_input_username = driver.find_element(By.XPATH, '//input[@placeholder="Username"]')
#     signup_input_username.send_keys(username)

#     signup_input_password = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
#     signup_input_password.send_keys(password)

#     # --- Step 3: Submit signup ---
#     signup_submit_btn = driver.find_element(By.XPATH, '//button[text()="Sign Up"]')
#     signup_submit_btn.click()

#     # --- Step 4: Handle alert after signup ---
#     WebDriverWait(driver, 10).until(EC.alert_is_present())  # Wait until browser shows alert
#     alert = driver.switch_to.alert
#     alert.accept()  # Click "OK" on the alert

#     time.sleep(2)  # (Small wait to avoid race condition)

#     # --- Step 5: Log in with new user and verify login button works  ---
#     login_btn = driver.find_element(By.XPATH, '//button[text()="Login"]')
#     login_btn.click()

#     login_input_username = driver.find_element(By.XPATH, '//input[@placeholder="Username"]')
#     login_input_username.send_keys(username)

#     login_input_password = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
#     login_input_password.send_keys(password)

#     login_btn = driver.find_element(By.XPATH, '//button[text()="Login"]')
#     assert login_btn.is_enabled()
#     assert login_btn.is_displayed()
#     login_btn.click()

#     time.sleep(5)  # Give some time for login

#     # --- Step 6: Create a product verify product product is visible---
#     product_input = driver.find_element(By.XPATH, '//input[@placeholder="Product Name"]')
#     assert product_input.is_displayed()
#     product_input.send_keys(product)

#     add_product_btn = driver.find_element(By.XPATH, '//button[text()="Create Product"]')
#     assert add_product_btn.is_displayed()
#     add_product_btn.click()

#     # --- Step 7: Verify product is added ---
#     product_list = driver.find_element(By.CLASS_NAME, "product-grid")
#     assert product in product_list.text
#     assert non_existing_product not in product_list.text 
#     assert product_list is not None
#     print("✅ Product added successfully!")
    
#     # --- Step 8: delete a Product Verify is gone ---
    
#     time.sleep(10)

#     # --- Teardown: Close browser ---
#     time.sleep(3)
#     driver.quit()
    
    
