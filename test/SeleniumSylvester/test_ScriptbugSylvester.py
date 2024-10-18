import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import traceback

driver = webdriver.Chrome()

try:
    # Navigate to the page with tabs
    driver.get("http://localhost:8080/lrr/")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # Login as a Lecturer
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "user")))
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.ID, "login_btn")
    
    username_input.send_keys("ashly@qq.com")
    password_input.send_keys("admin123")
    time.sleep(5)
    login_button.click()

    course_but= driver.find_element(By.XPATH, "(//div[@class='btn btn-default'])[1]")  # Adjust this XPATH as needed
    
    
    # Click on the alert
    course_but.click()
    time.sleep(5)

    marked_tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Marked']"))
    )
    marked_tab.click()

    # Wait for the Marked tab content to be present
    marked_tab_content = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='menu4' and contains(@class, 'active')]"))
    )

    time.sleep(5)
    remark_but = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Request remarking']"))
    )    
    remark_but.click()
    

    time.sleep(2) 

    # Switch to the alert
    alert = driver.switch_to.alert

    # Send keys to the prompt
    alert.send_keys("Number 2 was correct")

    # Accept the prompt (click OK)
    alert.accept()

    time.sleep(5)



except NoSuchElementException as e:
    print("NoSuchElementException: Could not find an element.")
    traceback.print_exc()
except TimeoutException as e:
    print("TimeoutException: An element took too long to load.")
    traceback.print_exc()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    traceback.print_exc()
finally:
    driver.quit()
