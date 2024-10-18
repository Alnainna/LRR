# Each time you run the test script reset the database.
# For this test script you won't need it since it changes
# the Ta's email and name automatically
import re
import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_restore_database(restore_database):
    assert restore_database is None


def createTA(driver, TA_name, emails, password):
    full_name = driver.find_element('name', 'fullname')
    full_name.send_keys(TA_name)
    email = driver.find_element('name', 'email')
    email.send_keys(emails)
    pas = driver.find_element('name', 'password')
    pas.send_keys(password)
    usr_type = driver.find_element('name', 'type')
    usr_type.click()
    click_create = driver.find_element('name', 'create_btn')
    click_create.click()


def login_lecturer(driver, url):
    # Open the website
    driver.get(url)
    driver.maximize_window()

    username_input = driver.find_element('name', "user")

    password_input = driver.find_element('name', "password")

    login_button = driver.find_element('id', "login_btn")

    # login as a Lecturer
    username_input.send_keys("admin@qq.com")
    password_input.send_keys("123")
    # Click the login button
    time.sleep(2)
    login_button.click()
    admin_tab = driver.find_element('id', 'admin_tab')
    admin_tab.click()

    cte_instructor = driver.find_element('id', 'tab_ins_accounts')
    cte_instructor.click()
    time.sleep(2)


def test_createTA(driver, url):
    driver_open = driver
    driver_open.maximize_window()
    login_lecturer(driver_open, url)
    try:
        fullname = "lanhuitest1"
        email = "lanhuitest1@qq.com"
        password = "new1452345678"
        createTA(driver_open, fullname, email,password)  # CREATE A TA  WITH FULLNAME lanhuitest1 email lanhuitest1@qq.com  password new1452345678

        get_output = WebDriverWait(driver_open, 20).until(
            EC.element_to_be_clickable((By.ID, "tab_ins_accounts"))
        )
        get_output.click()
        get_output_msg = driver_open.find_element(By.CLASS_NAME, "alert-warning")
        txt_alert = get_output_msg.text
        time.sleep(2)

        if txt_alert.find("TA user created successfully") == 0:
            logout_button = WebDriverWait(driver_open, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, 'nav-link') and contains(@href, 'logout.php')]"))
            )
            time.sleep(2)
            logout_button.click()
            time.sleep(2)
            username_input = driver_open.find_element('name', "user")
            password_input = driver_open.find_element('name', "password")
            login_button = driver_open.find_element('id', "login_btn")
            # login as the new TA
            username_input.send_keys(email)  # login with credentials of the created TA
            password_input.send_keys(password)
            # Click the login button
            time.sleep(2)

            login_button.click()

            time.sleep(2)
        elif txt_alert.find("Email address ") == 0:

            time.sleep(2)
            driver_open.quit()

        else:
            driver_open.quit()

        time.sleep(2)

    finally:
        driver_open.quit()


def test_generate_password(driver, url):
    driver_open = driver
    login_lecturer(driver_open, url)
    try:
        fullname = "lanhuitest2"
        email = "lanhuitest2@qq.com"
        password = ""
        createTA(driver_open, fullname, email,
                 password)  # CREATE A TA  WITH FULLNAME lanhuitest2 email lanhuitest2@qq.com  password ""

        get_output = WebDriverWait(driver_open, 20).until(
            EC.element_to_be_clickable((By.ID, "tab_ins_accounts"))
        )
        get_output.click()
        get_output_msg = driver_open.find_element(By.CLASS_NAME, "alert-warning")
        txt_alert = get_output_msg.text
        time.sleep(2)

        if txt_alert.find("TA user created successfully") == 0:
            time.sleep(2)
            email_pattern = r"Use email (\S+) as account name"
            password_pattern = r" (\S+)\ as password."
            email_match = re.search(email_pattern, txt_alert)
            password_match = re.search(password_pattern, txt_alert)
            if email_match and password_match:
                # Extract email and password from the matches
                email = email_match.group(1)
                password = password_match.group(1)
            logout_button = WebDriverWait(driver_open, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, 'nav-link') and contains(@href, 'logout.php')]"))
            )
            logout_button.click()
            time.sleep(2)
            username_input = driver_open.find_element('name', "user")
            password_input = driver_open.find_element('name', "password")
            login_button = driver_open.find_element('id', "login_btn")
            # login as the new TA
            username_input.send_keys(email)  # login with credentials of the created TA
            password_input.send_keys(password)
            # Click the login button
            time.sleep(2)

            login_button.click()

            time.sleep(2)

        elif txt_alert.find("Email address ") == 0:
            time.sleep(2)
            driver_open.quit()

        else:
            driver_open.quit()

        time.sleep(2)

    finally:
        driver_open.quit()


def test_existingTA(driver, url, restore_database):
    driver_open = driver
    login_lecturer(driver, url)
    try:
# Use email nreyes@example.com as account name and new1452345678 as password.
        fullname = "lanhuitest1"
        email = "lanhuitest1@qq.com"
        password = "new1452345678"
        createTA(driver_open, fullname, email,
                 password)  # CREATE A TA  WITH FULLNAME lanhuitest1 email lanhuitest1@qq.com  password new1452345678

        get_output = WebDriverWait(driver_open, 20).until(
            EC.element_to_be_clickable((By.ID, "tab_ins_accounts"))
        )
        get_output.click()
        get_output_msg = driver_open.find_element(By.CLASS_NAME, "alert-warning")
        txt_alert = get_output_msg.text
        time.sleep(2)

        if txt_alert.find("TA user created successfully") == 0:
            time.sleep(2)


        elif txt_alert.find("Email address ") == 0:
            time.sleep(2)
            driver_open.quit()

        else:
            driver_open.quit()

        time.sleep(2)

    finally:
        driver_open.quit()
