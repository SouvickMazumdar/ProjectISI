import time
import pandas as pd
from selenium import webdriver
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
    browser.minimize_window()
    url = "https://www.zaubacorp.com/"
    browser.get(url)

    try:
        # print("^^"*100)
        input_company = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='searchid']"))
        )
        input_company.send_keys(option_company)
        time.sleep(3)

        first_option = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='result']/div[1]"))
        )

        first_option.click()

        time.sleep(2)
        # print("^^" * 100)
        # OVERVIEW part
        content_div = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/section/div[1]/p"))
        )
        ans=content_div.text

        # print("^^" * 100)
        # COMPANY TABLE
        basic_info=WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/section/div[1]/div[1]/div/div/table/tbody"))
        )
        # print(basic_info)
        child_elements = basic_info.find_elements(By.TAG_NAME, "tr")
        # print(len(child_elements))
        basic_info_ar=[]
        for child in child_elements:
            k=child.find_elements(By.TAG_NAME,"td")
            left=k[0].text
            right=k[1].text
            # print(left,right,"&&&")
            basic_info_ar.append([left,right])
        basic_table=pd.DataFrame(basic_info_ar,columns=["Tag","Details"])
        basic_table.index=range(1,len(basic_table)+1)

        # print("^^" * 100)
        # DIRECTORS TABLE
        directors_info = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/section/div[1]/div[12]/div/div[1]/table/tbody"))
        )
        child_elements = directors_info.find_elements(By.TAG_NAME, "tr")
        directors_info_ar = []
        for child in child_elements:
            k = child.find_elements(By.TAG_NAME, "td")
            first = k[0].text
            second = k[1].text
            third = k[2].text
            fourth = k[3].text
            directors_info_ar.append([first,second,third,fourth])
        directors_table = pd.DataFrame(directors_info_ar,columns=["DIN","Director Name","Designation","Appointment Date"])
        directors_table.index=range(1,len(directors_table)+1)

        print("^^" * 100)
        # PAST DIRECTORS TABLE
        past_directors_info = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/section/div[1]/div[12]/div/div[2]/table/tbody"))
        )
        child_elements = past_directors_info.find_elements(By.TAG_NAME, "tr")
        past_directors_info_ar = []
        for child in child_elements:
            k = child.find_elements(By.TAG_NAME, "td")
            first = k[0].text
            second = k[1].text
            third = k[2].text
            fourth = k[3].text
            past_directors_info_ar.append([first,second,third,fourth])
        past_directors_table = pd.DataFrame(directors_info_ar,columns=["DIN","Director Name","Designation","Appointment Date"])
        past_directors_table.index=range(1,len(past_directors_table)+1)

        return ans,basic_table,directors_table,past_directors_table

    except Exception as e:
        print(e)
        browser.quit()
        return "","","",""
