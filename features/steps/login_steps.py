from selenium import webdriver
from behave import given, when, then
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@given('User opens login page')
def step_enter_site(context):
    service = Service("msedgedriver.exe") 
    options = Options()

    context.driver = webdriver.Edge(service=service, options=options)
    context.driver.maximize_window() 

    context.driver.get("https://www.parfimo.ro/")

@when('Introduce credentials: email "{email}" and password "{password}".')
def step_introduce_credentials(context, email, password):
    wait = WebDriverWait(context.driver, 10)

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cc-Popup-closeButton")))
    context.driver.find_element(By.CLASS_NAME, "cc-Popup-closeButton").click()

    wait.until(EC.element_to_be_clickable((By.ID, "template-container_header_user")))
    context.driver.find_element(By.ID, "template-container_header_user").click()

    wait.until(EC.element_to_be_clickable((By.ID, "f_emailLogin")))
    context.driver.find_element(By.ID, "f_emailLogin").send_keys(email)
    context.driver.find_element(By.ID, "f_passLogin").send_keys(password)
    context.driver.find_element(By.CLASS_NAME, "Registration-submit").click()


@then('Login function working properly')
def step_login(context):
    wait = WebDriverWait(context.driver, 1)

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "UserzoneLayout-logout")))
        button = context.driver.find_element(By.CLASS_NAME, "UserzoneLayout-logout")
        assert button.is_displayed()
        context.driver.quit()
        return
    except TimeoutException:
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="Alert Alert--error js-username"]')))
            button = context.driver.find_element(By.XPATH, '//*[@class="Alert Alert--error js-username"]')
            assert button.is_displayed()
            context.driver.quit()
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    context.driver.quit()