import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "11"
    options.device_name = "emulator-5554"
    options.app = "Microsoft_To_Do.apk"  
    options.app_package = "com.microsoft.todos"
    options.app_activity = "com.microsoft.todos.ui.LaunchActivity"
    options.automation_name = "UiAutomator2"
    
    # Start Appium driver
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    driver.implicitly_wait(10)  
    yield driver
    driver.quit()



def test_create_product(driver: WebDriver):
    
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.TextView[@content-desc='To Do List']"))
    ).click()

    driver.find_element(AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Add Task']").click()

    driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@resource-id='com.splendapps.splendo:id/edtTaskName']").send_keys("Test Product")

    driver.find_element(AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='Save Task']").click()

    assert "Product created successfully" in driver.page_source



def test_read_product_list(driver: WebDriver):
    product_list = WebDriverWait(driver, 10).until(
        lambda d: d.find_elements(AppiumBy.ACCESSIBILITY_ID, "productItem")
    )
    assert len(product_list) > 0, "Product list is empty"



def test_update_product(driver: WebDriver):

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "editButton"))
    ).click()
    
   
    name_input = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "productNameInput")
    name_input.clear()
    name_input.send_keys("Updated Product")
    

    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "saveButton").click()
    
    




def test_delete_product(driver: WebDriver):
  
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "deleteButton"))
    ).click()
    
   
if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
