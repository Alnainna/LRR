import time  # Import time module for waiting
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# New instance of the Chrome driver
driver = webdriver.Chrome()

try:
    # Step 1: Open the login page
    driver.get("http://localhost:8080/lrr/lrr/admin.php")  # Replace with your actual login page URL

    # Step 2: Wait for the login page to fully load and locate the "Sign Up" link
    sign_up_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signup_link"))
    )
    
    # Step 3: Click the "Sign Up" link to navigate to the sign-up page
    sign_up_link.click()

    # Step 4: Wait for the sign-up page to fully load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signup_form"))
    )

    # Step 5: Fill out the sign-up form
    driver.find_element(By.ID, "full_name").send_keys("John Doe")
    driver.find_element(By.ID, "student_id").send_keys("12345678")
    driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
    driver.find_element(By.ID, "password1").send_keys("Password123!")
    driver.find_element(By.ID, "password2").send_keys("Password123!")

    # Step 6: Submit the sign-up form
    driver.find_element(By.ID, "signup_btn").click()

    # Step 7: Wait for the sign-up result
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Check if sign-up failed
    if "alert-danger" in driver.page_source:
        print("Sign-up failed. Checking if form values are retained...")

        # Wait for a few seconds (adjust as needed)
        time.sleep(3)

        # Modify the student ID again
        driver.find_element(By.ID, "student_id").clear()
        driver.find_element(By.ID, "student_id").send_keys("87654321")

        # Verify if the other fields retain their values
        assert driver.find_element(By.ID, "full_name").get_attribute("value") == "John Doe"
        assert driver.find_element(By.ID, "email").get_attribute("value") == "john.doe@example.com"
        assert driver.find_element(By.ID, "password1").get_attribute("value") == ""
        assert driver.find_element(By.ID, "password2").get_attribute("value") == ""

        # Resubmit the form
        driver.find_element(By.ID, "signup_btn").click()

        # Wait for the result again
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Check for success or failure after second attempt
        if "alert-danger" in driver.page_source:
            print("Second sign-up attempt failed. Further investigation needed.")


            # Print the retained values
            print("Retained form values after second attempt:")
            print("Full Name:", driver.find_element(By.ID, "full_name").get_attribute("value"))
            print("Email:", driver.find_element(By.ID, "email").get_attribute("value"))
            # Password fields might be intentionally cleared, so they won't be printed here
            print("Modified Student ID:", driver.find_element(By.ID, "student_id").get_attribute("value"))
            
        else:
            print("Second sign-up attempt successful!")
    else:
        print("Sign-up successful!")

        

finally:
    # Close the browser
    driver.quit()