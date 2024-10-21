import time

import pandas as pd
import requests
# import pandas as pd
# from io import BytesIO
# from PIL import Image
# from PIL import ImageEnhance
# from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options

def content(option_company):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (for better performance)
    chrome_options.add_argument("--no-sandbox")  # Required if running as root
    browser= webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    # browser.minimize_window()
    url = 'https://www.tofler.in/'
    browser.get(url)
    try:
        # browser.minimize_window()
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
        ans=""
        try:
            content_div = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='overview'] div[class='card-content']"))
            )
            paragraphs = content_div.find_elements(By.TAG_NAME, 'p')
            ans = "\n\n".join([paragraph.text for paragraph in paragraphs])
        except Exception:
            pass











        # Network image
        image_data=""
        try:
            img_div=browser.find_element(By.ID,"companyNetwork")
            img_element=img_div.find_element(By.CLASS_NAME,"hide-on-print")
            img_url=img_element.get_attribute('src')

            image_data = requests.get(img_url).content
        except Exception:
            pass

        # with open('image.jpg', 'wb') as file:
        #     file.write(image_data)
        # print("%"*100)





        # Directors
        ans_dir=""
        ar=""
        try:
            content_div_dir = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "overview_directors"))
            )
            paragraphs_dir = content_div_dir.find_elements(By.TAG_NAME, 'p')
            l=[]
            for paragraph in paragraphs_dir:
                if paragraph.get_attribute("class") not in ["tml_dr_name","tml_dr_design"]:
                    print(paragraph.get_attribute("class"))
                    l.append(paragraph.text)
            ans_dir = "\n\n".join(l)

            director=browser.find_element(By.ID,"directors-time_line-view")
            child_elements=director.find_elements(By.CLASS_NAME, "timeline_card")
            ar=[]
            # print(len(child_elements),"$"*100)
            for child in child_elements:

                date = child.find_element(By.CLASS_NAME, "tml_year").text
                name = child.find_element(By.CLASS_NAME, "tml_dr_name").text
                role = child.find_element(By.CLASS_NAME, "tml_dr_design").text
                # print([date,name,role])
                ar.append([date, name, role])
        except Exception:
            pass



        # print(table)




        # Financial Part
        fin_ar=""
        try:
            browser.find_element(By.ID,"financials-tab").click()
            content_fin=browser.find_element(By.XPATH,"/html/body/main/div[1]/div[1]/div/div[3]/div[1]/div[1]/div/table/tbody")
            child_elements=content_fin.find_elements(By.TAG_NAME,"tr")
            child_elements=child_elements[1:-1]
            fin_ar=[]
            for child in child_elements:
                k=child.find_elements(By.TAG_NAME,"td")
                left=k[0].text
                right=k[1].text
                fin_ar.append([left,right])
        except Exception:
            pass

        # browser.maximize_window()
        # finance_div = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//a[@id='financials-tab']"))
        # )
        # finance_div.click()
        # time.sleep(1)
        # browser.execute_script("window.scrollBy(0, 240)")
        # time.sleep(4)
        #
        # zoom_level = 0.8
        # browser.execute_script(f"document.body.style.zoom='{zoom_level}';")
        # time.sleep(3)
        # specific_div = browser.find_element(By.XPATH, "//div[@id='financial-details-financial-tab']//div[@class='card-content']")  # Replace with your class or selector
        #
        # # Image Handling
        # specific_div.screenshot("div_image.png")
        # image = Image.open('div_image.png')
        # # location = specific_div.location
        # # size = specific_div.size
        #
        # # Cropping
        # # crop_box = (0, 60, 650, 510)# when chrome is opening during execution(left,up,right,down)
        # crop_box=(0,60,900,510)
        # # print(crop_box)
        # # print(location,size)
        # div_image=image.crop(crop_box)
        #
        # # image enhancement
        # # Contrast and sharpness and color enhanced
        # img_contrasted = ImageEnhance.Sharpness(ImageEnhance.Contrast(ImageEnhance.Color(div_image).enhance(3.5)).enhance(1.6)).enhance(1.6)
        #
        # img_byte_arr = BytesIO()
        # img_contrasted.save(img_byte_arr, format='PNG')
        # img_byte_arr.seek(0)  # Move to the beginning of the BytesIO object
        # # This line resets the pointer of the BytesIO stream back to the beginning.
        # # This is necessary if you want to read the data from the stream after writing to it,
        # # ensuring that any subsequent read operations start from the beginning of the stream.



        return ans,fin_ar,image_data,ans_dir,ar
    except Exception:
        browser.quit()
        return "","","","",""


