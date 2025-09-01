from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By   # ✅ Better way to locate elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# The URL where your frontend app is running
APP_URL = 'http://localhost:5173'

# Setup Chrome options (disable unnecessary logs)
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])


def test_create_new_user():
    """
    Full end-to-end test:
    1. Open the app
    2. Sign up a new user
    3. Log in with that user
    4. Create a product
    5. Verify the product is visible in the list
    """
    
    username = "testuserhannes"
    password = "testpassword"
    product = "Bajen Halsduk"  # Product name we want to create
    non_existing_product="Aik Tröja"

    # --- Arrange / Setup ---
    driver = webdriver.Chrome(options=options)
    driver.get(APP_URL)  # Open the app in the browser

    # --- Step 1: Navigate to Signup form ---
    signup_btn = driver.find_element(By.ID, "signup")
    signup_btn.click()

    # --- Step 2: Fill in signup form ---
    signup_input_username = driver.find_element(By.XPATH, '//input[@placeholder="Username"]')
    signup_input_username.send_keys(username)

    signup_input_password = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
    signup_input_password.send_keys(password)

    # --- Step 3: Submit signup ---
    signup_submit_btn = driver.find_element(By.XPATH, '//button[text()="Sign Up"]')
    signup_submit_btn.click()

    # --- Step 4: Handle alert after signup ---
    WebDriverWait(driver, 10).until(EC.alert_is_present())  # Wait until browser shows alert
    alert = driver.switch_to.alert
    alert.accept()  # Click "OK" on the alert

    time.sleep(2)  # (Small wait to avoid race condition)

    # --- Step 5: Log in with new user and verify login button works  ---
    login_btn = driver.find_element(By.XPATH, '//button[text()="Login"]')
    login_btn.click()

    login_input_username = driver.find_element(By.XPATH, '//input[@placeholder="Username"]')
    login_input_username.send_keys(username)

    login_input_password = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
    login_input_password.send_keys(password)

    login_btn = driver.find_element(By.XPATH, '//button[text()="Login"]')
    assert login_btn.is_enabled()
    assert login_btn.is_displayed()
    login_btn.click()

    time.sleep(5)  # Give some time for login

    # --- Step 6: Create a product verify product product is visible---
    product_input = driver.find_element(By.XPATH, '//input[@placeholder="Product Name"]')
    assert product_input.is_displayed()
    product_input.send_keys(product)

    add_product_btn = driver.find_element(By.XPATH, '//button[text()="Create Product"]')
    assert add_product_btn.is_displayed()
    add_product_btn.click()

    # --- Step 7: Verify product is added ---
    product_list = driver.find_element(By.CLASS_NAME, "product-grid")
    assert product in product_list.text
    assert non_existing_product not in product_list.text 
    assert product_list is not None
    print("✅ Product added successfully!")
    
    # --- Step 8: delete a Product Verify is gone ---
    
    time.sleep(10)

    # --- Teardown: Close browser ---
    time.sleep(3)
    driver.quit()
