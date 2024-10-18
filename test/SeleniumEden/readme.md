Sign-Up Automation Test Script
Overview
This script automates the sign-up process for a web application using Selenium WebDriver. It tests whether form values are retained correctly if the initial sign-up attempt fails and requires modification of the student ID before resubmission.

Prerequisites
Python 3
Selenium library
Chrome WebDriver
A running instance of the web application on http://localhost:8080

Configuration
Web Application URL: Make sure the web application is running at http://localhost:8080. Adjust the URL in the script if necessary.

Update Element Locators: Ensure the IDs used in the script (signup_link, signup_form, full_name, student_id, email, password1, password2, signup_btn) match those in your web application.

Run the script:

Script Logic

Open the Login Page: The script navigates to the login page of the web application.
Click the "Sign Up" Link: It waits for the "Sign Up" link to appear and clicks it to navigate to the sign-up page.
Fill Out the Sign-Up Form: It fills out the form fields (Full Name, Student ID, Email, Password).
Submit the Form: It submits the form and waits for the result.
Check for Sign-Up Failure: If sign-up fails, it checks if form values are retained.
Modify Student ID: If the form values are retained, it modifies the student ID and resubmits the form.
Verify Retained Values: It verifies if other fields retain their values after modifying the student ID.
Print Retained Values: If the second attempt is successful, it prints the retained form values.
Close the Browser: The browser is closed at the end of the script execution.



The script provides the following output:

Sign-Up Successful: Indicates the sign-up was successful on the first attempt.
Sign-Up Failed: Indicates the sign-up failed on the first attempt and checks for retained values.
Second Sign-Up Attempt Successful: Indicates the second sign-up attempt was successful and prints the retained values.
Second Sign-Up Attempt Failed: Indicates the second sign-up attempt also failed, suggesting further investigation is needed.
Notes
Form Field IDs: Ensure the IDs used in the script match those in your web application.
Password Fields: The script intentionally does not print password fields for security reasons.
Adjust Wait Times: Modify the wait times as needed depending on your application's response times.
Troubleshooting
Element Not Found: Verify the element IDs and update them in the script.
WebDriver Errors: Ensure the Chrome WebDriver is installed and matches your Chrome browser version.
Connection Errors: Ensure the web application is running and accessible at the specified URL.
Contributing
