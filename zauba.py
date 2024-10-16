import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (for better performance)
chrome_options.add_argument("--no-sandbox")  # Required if running as root

def content(option_company):
    browser = webdriver.Chrome()
    url = "https://www.zaubacorp.com/"
    browser.get(url)
    browser.maximize_window()
    input_company = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='searchid']"))
    )

    input_company.send_keys(option_company)
    time.sleep(1)
    try:
        first_option = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='result']/div[1]"))
        )

        first_option.click()

        time.sleep(2)

        # OVERVIEW part
        content_div = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='container information']"))
        )
        tot_text=content_div.text
        ans=tot_text[0:tot_text.find("Company Details")]#type of tot_text is string
        return ans,""
    except TimeoutException:
        browser.quit()
        return "",""
