import time
from io import BytesIO
from PIL import Image
from PIL import ImageEnhance
from selenium.common import TimeoutException
# from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (for better performance)
chrome_options.add_argument("--no-sandbox")  # Required if running as root

def content(option_company):
    browser = webdriver.Chrome(options=chrome_options)
    url = 'https://www.tofler.in/'
    browser.get(url)
    browser.maximize_window()
    input_company = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#searchbox"))
    )
    input_company.send_keys(option_company)
    time.sleep(1)
    input_company.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    input_company.send_keys(Keys.ENTER)
    time.sleep(2)

    # OVERVIEW part
    try:
        content_div = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='overview'] div[class='card-content']"))
        )
        paragraphs = content_div.find_elements(By.TAG_NAME, 'p')
        ans = "\n\n".join([paragraph.text for paragraph in paragraphs])
    except TimeoutException:
        browser.quit()
        return "",""


    # Financial Part
    try:
        finance_div = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='financials-tab']"))
        )
    except TimeoutException:
        browser.quit()
        return ans,""
    finance_div.click()
    time.sleep(1)
    browser.execute_script("window.scrollBy(0, 240)")
    time.sleep(3)

    zoom_level = 0.8
    browser.execute_script(f"document.body.style.zoom='{zoom_level}';")
    time.sleep(3)
    specific_div = browser.find_element(By.XPATH, "//div[@id='financial-details-financial-tab']//div[@class='card-content']")  # Replace with your class or selector

    # Image Handling
    specific_div.screenshot("div_image.png")
    image = Image.open('div_image.png')
    # location = specific_div.location
    # size = specific_div.size

    # Cropping
    # crop_box = (0, 60, 650, 510)# when chrome is opening during execution(left,up,right,down)
    crop_box=(0,60,900,510)
    # print(crop_box)
    # print(location,size)
    div_image=image.crop(crop_box)

    # image enhancement
    # Contrast and sharpness and color enhanced
    img_contrasted = ImageEnhance.Sharpness(ImageEnhance.Contrast(ImageEnhance.Color(div_image).enhance(3.5)).enhance(1.6)).enhance(1.6)

    img_byte_arr = BytesIO()
    img_contrasted.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Move to the beginning of the BytesIO object
    # This line resets the pointer of the BytesIO stream back to the beginning.
    # This is necessary if you want to read the data from the stream after writing to it,
    # ensuring that any subsequent read operations start from the beginning of the stream.

    return ans,img_byte_arr
