from selenium import webdriver
from behave import given, when, then
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given('User opens login page and wants to create a new account')
def step_enter_site(context):
    service = Service("msedgedriver.exe") 
    options = Options()

    context.driver = webdriver.Edge(service=service, options=options)
    context.driver.maximize_window() 

    context.driver.get("https://www.parfimo.ro/")

@when('Introduce credentials: email "{email}" and password "{password}"')
def step_introduce_credentials(context, email, password):
    wait = WebDriverWait(context.driver, 10)

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cc-Popup-closeButton")))
    context.driver.find_element(By.CLASS_NAME, "cc-Popup-closeButton").click()

    wait.until(EC.element_to_be_clickable((By.ID, "template-container_header_user")))
    context.driver.find_element(By.ID, "template-container_header_user").click()
    context.driver.find_element(By.XPATH, "//*[@class='Registration-link']").click()

    wait.until(EC.element_to_be_clickable((By.ID, "f_email")))
    context.driver.find_element(By.ID, "f_email").send_keys(email)
    context.driver.find_element(By.ID, "f_newPass").send_keys(password)
    context.driver.find_element(By.ID, "f_pass2").send_keys(password)
    context.driver.find_element(By.NAME, "register").click()

@then('Register succesful')
def step_register_successful(context):
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "UserzoneLayout-logout")))
    
    context.driver.quit()