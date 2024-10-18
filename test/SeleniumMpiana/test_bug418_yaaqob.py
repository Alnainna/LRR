import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from helper import login

@pytest.mark.parametrize("course_id, course_name, ta_name", [(1, "Teecloudy - Ashly Course Testing", "Mark")])
def test_assign_a_new_ta_to_a_course(course_id, course_name, ta_name, driver, url, admin_username, admin_password, restore_database):
    try:
        driver.maximize_window()

        login(driver, url, admin_username, admin_password)

        admin_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "admin_tab"))
        )
        admin_tab.click()
        
        # Locate the form and select the TA
        ta_form = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, f"//form[@id='drop_menu_form_{course_id}']"))
        )

        ta_dropdown = Select(ta_form.find_element(By.XPATH, ".//select[@name='ta']"))
        ta_dropdown.select_by_visible_text(ta_name)

        # Submit the form using JavaScript
        driver.execute_script("arguments[0].submit();", ta_form)

        # find table courses
        table_courses = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//*[@id='tab-existing-courses']/table"))
        )
        # find the row with matching course_name
        course_row = table_courses.find_element(By.XPATH, f".//tr[td='{course_name}']")
        # find the column with TA name
        ta_column = course_row.find_element(By.XPATH, ".//td[4]")

        # assert the TA name in the column
        assert ta_name in ta_column.text, f"Error: TA name {ta_name} not found in the column {ta_column.text}"
        
    except NoSuchElementException as e:
        return f"Error: {str(e)}"
    except UnexpectedAlertPresentException as e:
        return f"Error: {str(e)}"
    except AssertionError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        driver.quit()


@pytest.mark.parametrize("course_id, course_name, ta_name", [(1, "Teecloudy - Ashly Course Testing", "Mark")])
def test_assign_the_same_ta_to_the_same_course_twice(course_id, course_name, ta_name, driver, url, admin_username, admin_password, restore_database):
    try:
        driver.maximize_window()        
        login(driver, url, admin_username, admin_password)

        admin_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "admin_tab"))
        )
        admin_tab.click()

        # Hui: assign the TA for the first time
        # (1) Locate the form and select the TA
        ta_form = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH,
            f"//form[@id='drop_menu_form_{course_id}']")) )

        ta_dropdown = Select(ta_form.find_element(By.XPATH, ".//select[@name='ta']"))
        ta_dropdown.select_by_visible_text(ta_name)

        # (2) Submit the form using JavaScript
        driver.execute_script("arguments[0].submit();", ta_form)

        # (3) Find table courses
        table_courses_before = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//*[@id='tab-existing-courses']/table"))
        )
        # (4) Find the row with matching course_name
        course_row_before = table_courses_before.find_element(By.XPATH, f".//tr[td='{course_name}']")
        # (5) Find the column with TA name
        old_cell_content = course_row_before.find_element(By.XPATH, ".//td[4]").text


        # Hui: assign the same TA again
        ta_form = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, f"//form[@id='drop_menu_form_{course_id}']")))
        ta_dropdown = Select(ta_form.find_element(By.XPATH, ".//select[@name='ta']"))
        ta_dropdown.select_by_visible_text(ta_name)        
        driver.execute_script("arguments[0].submit();", ta_form)
        
        # Wait for an expected alert and accept it
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        
        # find table courses
        table_courses_after = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//*[@id='tab-existing-courses']/table"))
        )
        # find the row with matching course_name
        course_row_after = table_courses_after.find_element(By.XPATH, f".//tr[td='{course_name}']")
        # find the column with TA name
        new_cell_content = course_row_after.find_element(By.XPATH, ".//td[4]").text

        # assert the TA name in the column
        assert old_cell_content == new_cell_content, f"Error: TA name in the column has changed from {old_cell_content} to {new_cell_content}"
    
    except NoSuchElementException as e:
        return f"Error: {str(e)}"
    except UnexpectedAlertPresentException as e:
        return f"Error: {str(e)}"
    except AssertionError as e:
       return f"Error: {str(e)}"
    except Exception as e:
       return f"Error: {str(e)}"
    finally:
        driver.quit()
