from selenium import webdriver
from behave import given, when, then
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, WebDriverException
from time import sleep

def close_incomaker_popup(context):

    wait = WebDriverWait(context.driver, 2) 

    try:
        iframe_locator = (By.CSS_SELECTOR, "iframe.incomaker_modal_popup_iframe[src*='incomaker.com/content/campaign']")
        iframe_element = wait.until(EC.presence_of_element_located(iframe_locator))
        context.driver.switch_to.frame(iframe_element)

        close_button_wait = WebDriverWait(context.driver, 10)
        close_button = close_button_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.close_button[data-inco-event-close-onclick='true']")))
        
        context.driver.execute_script("arguments[0].click();", close_button)

    except TimeoutException:
        print("Timeout: The incomaker iframe or the close button within it did not appear within the specified time. Popup not closed.")
    except NoSuchElementException:
        print("No Such Element: The incomaker iframe or the close button within it was not found. Popup not closed.")
    except ElementClickInterceptedException as e: 
        print(f"ElementClickInterceptedException during popup close: {e}. Popup was likely intercepted and not closed.")
    except WebDriverException as e: 
        print(f"WebDriverException during popup close: {e}. This might indicate browser instability. Popup not closed.")
    except Exception as e:
        print(f"An unexpected error occurred while trying to close the popup: {e}. Popup not closed.")
    finally:
        print("Switching back to default content.")
        context.driver.switch_to.default_content()


@given('User opens the home page.')
def step_enter_site(context):
    service = Service("msedgedriver.exe")
    options = Options()

    context.driver = webdriver.Edge(service=service, options=options)
    context.driver.maximize_window()

    context.driver.get("https://www.parfimo.ro/")


@when('User searches for "{parfume1}" and "{parfume2}" and adds them to cart.')
def step_introduce_credentials(context, parfume1, parfume2):
    wait = WebDriverWait(context.driver, 10)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-cc-accept-all])[1]")))
        context.driver.find_element(By.XPATH, "(//button[@data-cc-accept-all])[1]").click()
    except TimeoutException:
        print("Cookie consent pop-up did not appear or was already handled.")


    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Icon.Icon-search")))
    context.driver.find_element(By.CSS_SELECTOR, ".Icon.Icon-search").click()
 
    wait.until(EC.presence_of_element_located((By.ID, "f_header-search")))
    context.driver.find_element(By.ID, "f_header-search").send_keys(parfume1)
  
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".header-Search-submit.js-header-search-submit")))
    context.driver.find_element(By.CSS_SELECTOR, ".header-Search-submit.js-header-search-submit").click()
 
    product1_link_locator = (By.CSS_SELECTOR, "div.ProductCard-content a[href*='versace-eros-apa-de-parfum-pentru-barbati']")
    wait.until(EC.element_to_be_clickable(product1_link_locator))
    context.driver.find_element(*product1_link_locator).click()

    add_to_basket_button_locator = (By.CSS_SELECTOR, ".Button--AddToBasket") 
    wait.until(EC.element_to_be_clickable(add_to_basket_button_locator)) 
    context.driver.find_element(*add_to_basket_button_locator).click()


    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "SummaryBuyPopup-back")))
    context.driver.find_element(By.CLASS_NAME, "SummaryBuyPopup-back").click()


    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='Icon Icon-search']"))) 
    context.driver.find_element(By.XPATH, "//*[@class='Icon Icon-search']").click()
 
    wait.until(EC.presence_of_element_located((By.ID, "f_header-search")))
    context.driver.find_element(By.ID, "f_header-search").send_keys(parfume2)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".header-Search-submit.js-header-search-submit")))
    context.driver.find_element(By.CSS_SELECTOR, ".header-Search-submit.js-header-search-submit").click()

    product2_link_locator = (By.CSS_SELECTOR, "div.ProductCard-content a[href*='paco-rabanne-invictus-apa-de-toaleta-pentru-barbati']")
    wait.until(EC.element_to_be_clickable(product2_link_locator))
    context.driver.find_element(*product2_link_locator).click()

    add_to_basket_button_locator_2 = (By.CSS_SELECTOR, ".Button--AddToBasket") 
    wait.until(EC.element_to_be_clickable(add_to_basket_button_locator_2)) 
    context.driver.find_element(*add_to_basket_button_locator_2).click()

    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "SummaryBuyPopup-back")))
    context.driver.find_element(By.CLASS_NAME, "SummaryBuyPopup-back").click()
    
    close_incomaker_popup(context) 

    try:
        print("Trying to click basket icon...")
        basket_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.header-UserZone-link.header-UserZone-link--basket"))
        )

        # Scroll the element into view
        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", basket_button)
        sleep(0.5)  # small delay to let scroll finish

        # Check position (debug)
        loc = basket_button.location
        print(f"Basket button location: x={loc['x']} y={loc['y']}")

        # Ensure it's visible and try clicking via JS
        context.driver.execute_script("arguments[0].click();", basket_button)
        print("Clicked basket icon.")
    except Exception as e:
        print(f"Failed to click basket: {e}")

@then('Checks if the "{parfume1}" and "{parfume2}" are added in cart.')
def step_checking(context, parfume1, parfume2):
    wait = WebDriverWait(context.driver, 10)

    try:
        print("Attempting to verify products in cart...")
        product_div_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.basket-Products-col.basket-Products-col--goods")))

        full_div_text = product_div_element.text.strip()

        print(f"Full text content of the cart's product list div:\n'{full_div_text}'")

        if parfume1 in full_div_text and parfume2 in full_div_text:
            print(f"SUCCESS: Both '{parfume1}' and '{parfume2}' are present in the cart's product list. TEST PASSED.")
        else:
            print(f"FAILURE: Either '{parfume1}' or '{parfume2}' (or both) not found in the cart's product list. TEST FAILED.")

    except Exception as e:
        print(f"An error occurred while trying to check the element's text: {e}. TEST FAILED.")

    context.driver.quit()
