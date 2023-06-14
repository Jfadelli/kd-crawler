import csv
import time
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# set env var,
user_name = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")

#initialize web driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# set env var,
user_name = os.environ.get("USER_NAME")
password = os.environ.get("PASSWORD")


# Navigate to the website
driver.get("https://www.kdealer.com")

# check to see if not logged in
# Identify and interact with web elements
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'main-container')))
current_url = driver.current_url

def login(current_url, login_attempts):
    if 'b2clogin' in current_url:
        login_attempts += 1
        print(login_attempts)
        try:
            username_input = wait.until(
                EC.presence_of_element_located((By.ID, "signInName"))
            )
            password_input = wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            submit_button = wait.until(
                EC.element_to_be_clickable((By.ID, "next"))
            )

            username_input.send_keys(user_name)
            password_input.send_keys(password)
            submit_button.click()
            time.sleep(3)
            if "commonDashboard" in driver.current_url:
                print('success')
            
        except:
            print('Login failed')
        
        print('Login successful - proceed to vehicle locator')

login(current_url, 0)
    
    # navigate to vehicle locator
try:
    driver.get('https://www.kdealer.com/VehicleLocator')
    year_selector_dropdown = wait.until(
        EC.presence_of_element_located((By.ID, 'year')))
    year_selector_dropdown.click()
    year_selection = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-value="2023"]')))
    year_selection.click()
    print('year selection success')
    print('series selection begin')
    # -------------------------------------------------


    def select_option_from_dropdown(driver, dropdown_locator, option_locator, option):
        # Open the dropdown menu
        dropdown_element = driver.find_element(*dropdown_locator)
        dropdown_element.click()

        # Scroll to the desired option
        option_element = driver.find_element(*option_locator)
        actions = ActionChains(driver)
        actions.move_to_element(option_element)
        actions.perform()

        # Wait until the option is visible and clickable
        wait = WebDriverWait(driver, 100)
        wait.until(EC.visibility_of_element_located(option_locator))
        wait.until(EC.element_to_be_clickable(option_locator))


        # Select the option
        option_locator.click()

    # Define the locators for the dropdown and option elements
    dropdown_locator = ((By.ID, 'series'))
    option_locator = ((By.XPATH, "//li[contains(span/text(), 'J: TELLURIDE')]"))

    # Call the function to select the option from the dropdown
    select_option_from_dropdown(driver, dropdown_locator, option_locator)


    show_more_button = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'moreLessText')))
    show_more_button.click()

    # vehicle_status_drop_down = wait.until(
    #      EC.presence_of_element_located((By.ID,"status")))
    # vehicle_status_drop_down.click()
    # vehicle_status = wait.until(
    #      EC.presence_of_element_located((By.CSS_SELECTOR, 'data-value="DS"')))
    # vehicle_status.click()
    print('pass')
    
except:
    # driver.quit()
    print('vehicle locator fail')

    
# Write information to CSV

# with open("output.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Header1", "Header2"])  # Write headers if necessary
#     writer.writerow(['text', "Additional data"])

# Clean up resources
# driver.quit()s