from actor import Actor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import traceback

class Student(Actor):

	"""
	This class contains all the major scenarios a student system actor can execute
	automated by Selenium framework.

	Attributes:
	- password: password string.
	- student_id: student ID number.
	- utility: a utility object of the MyUtility class.

	Methods:
	- signup(): automates student registration process.
	- join_course(): automates student joining a course created by instructor.
	- submit_assignment(): automates student assignment submission process.
	- request_remarking(): automates student requesting lab report remarking request.
	- create_course_group(): automates student creating course group.
	- join_course_group(): automates student joining course group.

	TODO:
	- join_course_group()
	"""

	def __init__(self, password, student_id, utility):
		super().__init__(password, student_id)
		self.utility = utility

	def join_course(self):
		
		""" This metohd automates student joining a course created by instructor.

		Returns:
		- driver: selenium.webdriver object, or
		- 1 on failure to complete case execution.

		"""
		try:
			#Login in order to join a course.
			driver = self.utility.login(self)

			#Search for course by its code.
			wait = WebDriverWait(driver, 10)
			course_code_field = wait.until(EC.presence_of_element_located((By.ID, "search_field")))
			course_code = self.utility.getCourseCode()
			course_code_field.send_keys(course_code)
			find_btn = driver.find_element(By.ID, "find_btn")
			find_btn.click()

			#Wait until the course is found, and join.
			wait2 = WebDriverWait(driver, 10)
			join_btn = wait2.until(EC.element_to_be_clickable((By.ID, "join_btn")))
			join_btn.click()

			#If joined course successfully, proceed.
			wait3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/span")))
			return 0

		#Else, if exception happened, abort.
		except:
			print("There was a problem executing this test case")
			print("Error in \"join_course()\" method, see error_log.txt for more details")
			err_msg = traceback.format_exc()
			self.utility.log_error(err_msg)
			print("Treminating session")
			self.utility.killSession(driver)
			return 1
	def submit_assignment(self):

		""" This method automates student assignment submission process.

		Returns:
		- 0 on success.
		- 1 on failure to complete case execution.

		"""
		try:
			#Join the course to submit assignmment.
			driver = self.utility.login(self)

			#Navigate to course page.
			self.utility.open_course_page(driver)

			#Locate and click assignment submission button.
			wait2 = WebDriverWait(driver, 10)
			assignment_card = wait2.until(EC.element_to_be_clickable((By.ID, "submit_lab_report_btn")))
			assignment_card.click()

			#Locate the assignment submission form and fill in the required data.
			wait3 = WebDriverWait(driver, 10)
			assignment_form = wait3.until(EC.presence_of_element_located((By.ID, "submit_lab_report_form")))
			title = assignment_form.find_element(By.ID, "title")
			dateStr = self.utility.getTodayDate()
			timeStr = self.utility.getTime()
			title.send_keys("TESTSUBMISSIOM"+dateStr+timeStr)
			attachment = assignment_form.find_element(By.ID, "attachment1")
			attachment.send_keys(os.getcwd()+"/DUMMY_SUBMISSION.txt")
			submit = driver.find_element(By.ID, "submit_lab_assignment_btn")
			submit.click()
			return 0

		except:
			print("There was a problem executing this test case")
			print("Error in \"submit_assignment()\" method, see error_log.txt for more details")
			err_msg = traceback.format_exc()
			self.utility.log_error(err_msg)
			print("Treminating session")
			self.utility.killSession(driver)
			return 1

	def request_remarking(self):

		""" This method automates student creating course group.

		Returns:
		- 0 on success.
		- 1 on failure to complete case execution.		

		"""

		try:
			#Login in order to proceed to remarking request.
			driver = self.utility.login(self)
			
			#Locate the course by its code and open the course page.
			self.utility.open_course_page(driver)

			#Locate the remarking request button and click it.
			wait2 = WebDriverWait(driver, 10)
			marked_tab = wait2.until(EC.presence_of_element_located((By.ID, "marked_tab")))
			marked_tab.click()
			req_remark = driver.find_element(By.ID, "request_remarking_btn")
			req_remark.click()

			#Fill in the remarking form and submit.
			wait3 = WebDriverWait(driver, 10)
			alert = wait3.until(EC.alert_is_present())
			alert.send_keys("TESTREASON")
			alert.accept()
			return 0

		except:
			print("There was a problem executing this test case")
			print("Error in \"request_remarking()\" method, see error_log.txt for more details")
			err_msg = traceback.format_exc()
			self.utility.log_error(err_msg)
			print("Treminating session")
			self.utility.killSession(driver)
			return 1

	def create_course_group(self):
		
		""" This method automates student requesting lab report remarking request.

		Returns:
		- 0 on success.
		- 1 on failure to complete case execution.

		"""
		try:
			#Login in order to create course group.
			driver = self.utility.login(self)

			#Locate the course in which the group to be created.
			self.utility.open_course_page(driver)

			#Locate the create course group button and click it.
			wait2 = WebDriverWait(driver, 10)
			create_group = wait2.until(EC.presence_of_element_located((By.ID, "create_group_btn")))
			create_group.click()

			#Fill in the course group form and create.
			wait3 = WebDriverWait(driver, 10)
			group_form = wait3.until(EC.presence_of_element_located((By.ID, "frm")))
			timeStr = self.utility.getTime()
			dateStr = self.utility.getTodayDate()
			group_name = group_form.find_element(By.ID, "group_name")
			group_name.send_keys("TESTGROUP"+str(dateStr)+str(timeStr))
			create = driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/button[1]")
			create.click()
			return 0

		except:
			print("There was a problem executing this test case")
			print("Error in \"create_course_group()\" method, see error_log.txt for more details")
			err_msg = traceback.format_exc()
			self.utility.log_error(err_msg)
			print("Treminating session")
			self.utility.killSession(driver)
			return 1

	def join_course_group(self):
		pass