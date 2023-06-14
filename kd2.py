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
        
login(current_url, 0)
    
    # navigate to vehicle locator
try:
    driver.get('https://www.kdealer.com/VehicleLocator')

    year_selector_dropdown = wait.until(
        EC.presence_of_element_located((By.ID, 'year')))
    year_selector_dropdown.click()
    time.sleep(.5)
    year_selection = wait.until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-value="2023"]')))
    year_selection.click()
    time.sleep(1)    

    series_dropdown_menu = wait.until(
        EC.presence_of_element_located((By.ID, 'series')))
    series_dropdown_menu.click()
    time.sleep(.2)
    series_selection =wait.until(
        EC.presence_of_element_located((By.XPATH,"//li[@class='MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-1i5c738' and @data-value='J']")))
    driver.execute_script("arguments[0].scrollIntoView();", series_selection)
    series_selection.click()
    time.sleep(.2)

    show_more_button = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'moreLessText')))
    show_more_button.click()
    time.sleep(.2)

    vehicle_status_drop_down = wait.until(
         EC.presence_of_element_located((By.ID,"status")))
    vehicle_status_drop_down.click()
    time.sleep(.2)
    vehicle_status = wait.until(
         EC.presence_of_element_located((By.XPATH, '//li[@class="MuiButtonBase-root MuiMenuItem-root MuiMenuItem-gutters MuiMenuItem-root MuiMenuItem-gutters css-1i5c738" and @data-value="DS"]'))
        )
    vehicle_status.click()
    time.sleep(.1)

    search_button = wait.until(
        EC.presence_of_element_located((By.XPATH, '//button[@name="search" and @type="button" and contains(@class, "primary-btn")]'))
        )
    search_button.click()
    time.sleep(4)
except:
    print('vehicle locator fail')

# Write table information to CSV
try:
    # Find the table element
    table = driver.find_element(By.XPATH, '//table[@class="table table-responsive-sm"]')

    # Find all rows in the table body
    rows = table.find_elements(By.XPATH,"//tbody/tr")

    # Create a CSV file and write the table data to it
    with open("table_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        
        # Write the table header row
        header_row = table.find_element(By.XPATH,".//thead/tr")
        header_data = [th.text for th in header_row.find_elements(By.XPATH,".//th")]
        writer.writerow(header_data)

        # Write the table body rows
        for row in rows:
            row_data = [td.text for td in row.find_elements(By.XPATH,".//td")]
            writer.writerow(row_data)
        time.sleep(3)
        
except:
    print('export failed')


driver.quit()