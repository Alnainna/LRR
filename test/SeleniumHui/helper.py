from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException


def login(driver, url, username, password):
    try:
        driver.get(url)

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
    except (NoSuchElementException, UnexpectedAlertPresentException) as e:
        return f"Error: {str(e)}"


def logout(driver):
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class, 'nav-link') and contains(@href, 'logout.php')]")
        )
    )
    logout_button.click()