import time

import pandas as pd
import requests
# import pandas as pd
# from io import BytesIO
# from PIL import Image
# from PIL import ImageEnhance
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import base64
from IPython.display import HTML, display_html

# Set up Chrome options
def content(option_company):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (for better performance)
    chrome_options.add_argument("--no-sandbox")  # Required if running as root
    browser= webdriver.Chrome(options=chrome_options)

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
            try:
                browser.find_element(By.XPATH,"/html/body/section[5]/section[2]/div[1]/div[1]/p").click()
            except Exception:
                pass

            content_div = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/section[5]/section[2]/div[1]/div[1]/div[3]"))
            )
            paragraphs = content_div.find_elements(By.TAG_NAME, 'p')
            ans = "\n\n".join([paragraph.text for paragraph in paragraphs])
        except Exception:
            pass










        # Registration Details
        reg_d=""
        try:
            reg_div=browser.find_element(By.ID,"registered-details-module")
            reg=reg_div.find_element(By.CLASS_NAME,"registered_box_wrapper")
            child_reg=reg.find_elements(By.TAG_NAME,"div")
            reg_d = []
            for child in child_reg:
                left=child.find_element(By.TAG_NAME,"h3")
                right=child.find_element(By.TAG_NAME,"span")
                reg_d.append([left.text,right.text])
            ext=reg_div.find_element(By.CLASS_NAME,"gap-4")
            child_ext=ext.find_elements(By.TAG_NAME,"div")
            kt=["Type"]
            st=""
            for child in child_ext:
                st=st+child.text+","
            kt.append(st[0:-1])
            reg_d.append(kt)
        except Exception:
            pass

        # Directors
        ar=""
        try:
            director_div=browser.find_element(By.ID,"people-module")
            director=director_div.find_element(By.TAG_NAME,"tbody")
            child_elements=director.find_elements(By.TAG_NAME, "tr")
            ar=[]
            # print(len(child_elements),"$"*100)
            for child in child_elements:
                td_child=child.find_elements(By.TAG_NAME,"td")
                des = td_child[0].text
                name = td_child[1].text
                if name.find('\n')!=-1:
                    name=name[0:name.find('\n')]
                din = td_child[2].text
                tenure = td_child[3].text
                ar.append([des, name, din, tenure])
        except Exception:
            pass


        # Charges on asset
        asset_table=""
        try:
            tar_ass=browser.find_element(By.XPATH,"/html/body/section[5]/section[13]/div/div[2]/div[1]/div[1]")
            child_asst=tar_ass.find_elements(By.CLASS_NAME,"mobile-hide")
            asset_table=[]
            for child in child_asst:
                sub_child=child.find_element(By.CLASS_NAME,"flex-col")
                sub_child=sub_child.find_elements(By.TAG_NAME,"p")
                one=sub_child[0].text
                two=sub_child[1].find_element(By.TAG_NAME,"span").text
                three=sub_child[2].find_element(By.TAG_NAME,"span").text
                asset_table.append([one,two,three])
            print(asset_table)
        except Exception:
            pass




        # Key Metrics
        key_table=""
        try:
            key_div=browser.find_element(By.XPATH,"/html/body/section[5]/section[2]/div[3]/div[1]/div[2]/div[2]")
            key_child=key_div.find_elements(By.CLASS_NAME,"flex-col")
            key_table=[]
            for child in key_child:
                one=child.find_element(By.CLASS_NAME,"font-regular").text
                two=child.find_element(By.CLASS_NAME,"text-dark").text
                three=child.find_element(By.CLASS_NAME,"text-sm").text
                if one.find("GET PRO")!=-1 or two.find("GET PRO")!=-1 or three.find("GET PRO")!=-1:
                    key_table=""
                    raise
                key_table.append([one,two,three])
        except Exception:
            pass

        # Financial Part
        fin_ar=""
        try:
            # browser.find_element(By.ID,"financials-tab").click()
            fin_tab=browser.find_element(By.XPATH,"/html/body/section[5]/section[9]/div/div[2]/div[1]/table/tbody")
            child_elements=fin_tab.find_elements(By.TAG_NAME,"tr")
            # child_elements=child_elements[1:-1]
            fin_ar=[]
            for child in child_elements:
                k=child.find_elements(By.TAG_NAME,"td")
                # print(k)
                one=k[0].text
                two=k[1].text
                three=k[2].text
                four=k[3].text
                five=k[4].text
                six=k[5].text
                if one.find("GET PRO")!=-1 or two.find("GET PRO")!=-1 or three.find("GET PRO")!=-1 or four.find("GET PRO")!=-1 or five.find("GET PRO")!=-1 or six.find("GET PRO")!=-1:
                    fin_ar=""
                    raise
                fin_ar.append([one,two,three,four,five,six])
            # print(fin_ar,"%^"*100)
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



        return ans,fin_ar,key_table,reg_d,ar,asset_table
    except Exception:
        browser.quit()
        return "","","","","",""


