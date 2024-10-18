import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

# New instance of the Chrome driver
driver = webdriver.Chrome()

# Open the login page
driver.get("http://localhost/lrr/admin.php")

# Credentials for login
username = "lanhui@qq.com"
password = "admin123"

def login(driver, username, password):
    try:
        # Fill in the login form
        user_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "user_name"))
        )
        user_input.send_keys(username)

        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "user_password"))
        )
        password_input.send_keys(password)

        # Click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login_btn"))
        )
        login_button.click()

        # Wait for the admin_tab to become clickable
        admin_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "admin_tab"))
        )

        return True

    except (NoSuchElementException, UnexpectedAlertPresentException) as e:
        return f"Error: {str(e)}"

# Call the login function
login_result = login(driver, username, password)

# Click on admin_tab after successful login
if login_result:
    admin_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "admin_tab"))
    )
    admin_tab.click()

    # Optionally, wait for the Admin.php page to load
    admin_url = "http://localhost/lrr/Admin.php"
    WebDriverWait(driver, 15).until(
        EC.url_to_be(admin_url)
    )

print(login_result)

def assign_ta(driver, course_id, ta_name):
    try:
        # Locate the form and select the TA
        ta_form = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, f"//form[@id='drop_menu_form_{course_id}']"))
        )

        ta_dropdown = Select(ta_form.find_element(By.XPATH, ".//select[@name='ta']"))
        ta_dropdown.select_by_visible_text(ta_name)

        # Submit the form using JavaScript
        driver.execute_script("arguments[0].submit();", ta_form)

        # Wait for an expected alert and accept it
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        return alert_text

    except UnexpectedAlertPresentException as e:
        # Unexpected alert, handle it as an error
        return f"Error: Unexpected alert - {str(e)}"

    except (NoSuchElementException, Exception) as e:
        return f"Error: {str(e)}"



# The courses and test cases to test
courses_to_test = [
    {"id": 1, "name": "Teecloudy - Ashly Course Testing", "ta_assignments": {"JAMES": "Ta assigned successfully."}},
    {"id": 2, "name": "P.M2019 - Project Management", "ta_assignments": {"JAMES": "The selected TA is already assigned to this course."}},
]

# Execute the tests
@pytest.mark.parametrize("course", courses_to_test)
def test_assign_ta(course):
    for ta_name, expected_result in course["ta_assignments"].items():
        alert_text = assign_ta(driver, course["id"], ta_name) 
        # ----- ---- Print the raw strings for debugging ----- ---- --- 
        test_case_number = courses_to_test.index(course) + 1
        print(f"Test Case {test_case_number} - {course['name']} -- {ta_name}: Expected Result={expected_result}, Actual Alert Text={alert_text}")

        # Determine the result based on the comparison
        if expected_result.lower() in alert_text.lower():
            result = "Passed"
        else:
            result = "Failed"

        # Write the result to a test file with test case number ---
        with open("test_results.txt", "a") as file:
            file.write(f"Test Case {test_case_number} - {course['name']} -- {ta_name}: Result={result}, Expected Result={expected_result}, Actual Alert Text={alert_text}\n")

        # Print the result to the console --- 
        print(f"Test Case {test_case_number} - {course['name']} -- {ta_name}: Result={result}, Expected Result={expected_result}, Actual Alert Text={alert_text}")

        assert result == "Passed", f"Test Case {test_case_number} failed: Result={result}, Expected Result={expected_result}, Actual Alert Text={alert_text}"
