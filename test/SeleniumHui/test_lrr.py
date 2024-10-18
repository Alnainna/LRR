from helper import login, logout
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_admin_can_create_lecturer_account(driver, url, admin_username, admin_password, restore_database):
    # Administrator (admin@qq.com, password 123) logs in
    driver.maximize_window()
    login(driver, url, admin_username, admin_password)

    # Create a Lecturer account for Mr Lan (mrlan@qq.com, password [123Abc!])
    tab = driver.find_element(By.ID, 'tab_ins_accounts')
    tab.click()
    elem = driver.find_element(By.NAME, 'fullname')
    elem.send_keys('Mr Lan')
    elem = driver.find_element(By.NAME, 'email')
    elem.send_keys('mrlan@qq.com')
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys('123Abc!!')
    radio_button = driver.find_element(By.NAME, 'type')
    radio_button.click()
    button = driver.find_element(By.NAME, 'create_btn')
    button.click()

    # Log out Admin account
    logout(driver)

    # Log in Lecturer account
    login(driver, url, 'mrlan@qq.com', '123Abc!!')
    elems = driver.find_elements(By.CLASS_NAME, 'nav-link')
    assert '(Lecturer)' in elems[0].text
    assert 'Mr Lan' in elems[0].text
    driver.quit()


def test_lecturer_can_create_course(driver, url, restore_database):
    # Lecturer lanhui@qq.com logs in
    driver.maximize_window()
    login(driver, url, 'lanhui@qq.com', '123')

    # Create a course called CSC1001 Advanced Software Engineering, 2024
    elem = driver.find_element(By.NAME, 'name')
    elem.send_keys('Advanced Software Engineering')
    elem = driver.find_element(By.NAME, 'code')
    elem.send_keys('CSC1001')
    elem = driver.find_element(By.NAME, 'academic')
    elem.send_keys('2004')
    elem = driver.find_element(By.NAME, 'faculty')
    elem.send_keys('School of Computer Science and Technology')
    elem = driver.find_element(By.CLASS_NAME, 'btn-primary')
    elem.click()
    elems = driver.find_elements(By.CLASS_NAME, 'btn-default')
    last_elem = elems[-1]
    assert 'Advanced Software Engineering' in last_elem.text
    assert '(CSC1001)' in last_elem.text

    # Logout
    logout(driver)
    driver.quit()


def test_lecturer_can_post_assignment(driver, url, restore_database):
    # Lecturer lanhui@qq.com logs in
    driver.maximize_window()
    login(driver, url, 'lanhui@qq.com', '123')

    # Create an assignment called Take-home quiz 1 for course (P.M2019) - Project Management
    elems = driver.find_elements(By.CLASS_NAME, 'btn-default')
    elems[1].click()
    elem = driver.find_element(By.NAME, 'deadlinedate')
    elem.send_keys('002024/12/30')
    elem = driver.find_element(By.NAME, 'deadlinetime')
    elem.send_keys('23:59')
    elem = driver.find_element(By.NAME, 'title')
    elem.send_keys('Take-home quiz 1')
    elem = driver.find_element(By.NAME, 'instructions')
    elem.send_keys('This is a closed-book quiz.')
    elem = driver.find_element(By.NAME, 'marks')
    elem.send_keys('10')
    radio_button = driver.find_element(By.NAME, 'type')
    radio_button.click()
    elem = driver.find_element(By.CLASS_NAME, 'btn-primary')
    elem.click()

    # Check if the assignment has been successfully posted
    elem = driver.find_element(By.CLASS_NAME, 'card-title')
    assert 'Take-home quiz 1 (10 Marks, Individual)' in elem.text
    elem = driver.find_element(By.CLASS_NAME, 'text-muted')
    assert 'Deadline: 2024-12-30' in elem.text
    driver.quit()


def test_lecturer_can_add_student_numbers(driver, url, restore_database):
    # Lecturer lanhui@qq.com logs in
    driver.maximize_window()
    login(driver, url, 'lanhui@qq.com', '123')

    # Add ASE student numbers
    student_numbers = '''
    202420781739
    202420781740
    202420781741
    202420781742
    202420781743
    202420781745
    202420581366
    202420581368
    202420581369
    202420581370
    202420581372
    202420581373
    202420581374
    202420581376
    202420581378
    202420581381
    '''
    elem = driver.find_element(By.ID, 'admin_tab')
    elem.click()
    elem = driver.find_element(By.NAME, 'users')
    elem.send_keys(student_numbers)
    elem = driver.find_element(By.ID, 'register_btn')
    elem.click()

    elems = driver.find_elements(By.CSS_SELECTOR, 'p')
    added = 0
    student_lst = [number.strip() for number in student_numbers.strip().split('\n')]
    print(student_lst)
    for student_no in student_lst:
        for elem in elems:
            if student_no in elem.text and 'added' in elem.text:
                added += 1
                break
    assert added == len(student_lst)
    driver.quit()


def test_student_with_valid_student_number_can_sign_up(driver, url, restore_database):
    # Student with recognizable student number 202400000001 can sign up an account
    driver.get(url)
    driver.maximize_window()
    elem = driver.find_element(By.ID, 'signup_link')
    elem.click()
    elem = driver.find_element(By.NAME, 'fullname')
    elem.send_keys('Good Student')
    elem = driver.find_element(By.NAME, 'user_student_id')
    elem.send_keys('202400000001')
    elem = driver.find_element(By.NAME, 'email')
    elem.send_keys('goodstudent@qq.com')
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys('[123Abc]')
    elem = driver.find_element(By.NAME, 'confirmpassword')
    elem.send_keys('[123Abc]')
    elem = driver.find_element(By.ID, 'signup_btn')
    elem.click()
    logout(driver)

    # Log in Student account
    login(driver, url, '202400000001', '[123Abc]')
    elems = driver.find_elements(By.CLASS_NAME, 'nav-link')
    assert 'Student ID' in elems[0].text
    assert 'Good Student' in elems[0].text
    driver.quit()


def test_student_with_invalid_student_number_cannot_sign_up(driver, url, restore_database):
    # Student with unrecognizable student number cannot sign up an account
    driver.get(url)
    driver.maximize_window()
    elem = driver.find_element(By.ID, 'signup_link')
    elem.click()
    elem = driver.find_element(By.NAME, 'fullname')
    elem.send_keys('Good Student')
    elem = driver.find_element(By.NAME, 'user_student_id')
    elem.send_keys('202400000002')
    elem = driver.find_element(By.NAME, 'email')
    elem.send_keys('goodstudent@qq.com')
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys('[123Abc]')
    elem = driver.find_element(By.NAME, 'confirmpassword')
    elem.send_keys('[123Abc]')
    elem = driver.find_element(By.ID, 'signup_btn')
    elem.click()

    # Log in Student account
    login(driver, url, '202400000002', '[123Abc]')
    elems = driver.find_elements(By.CLASS_NAME, 'nav-link')
    assert not 'Student ID' in elems[0].text
    assert not 'Good Student' in elems[0].text
    driver.quit()


@pytest.mark.skip()
def test_student_can_join_course():
    # Student can join CSC1001 Advanced Software Engineering
    assert True


@pytest.mark.skip()
def test_student_can_submit_assignment():
    # Student can submit Take-home quiz 1 for CSC1001
    assert True
