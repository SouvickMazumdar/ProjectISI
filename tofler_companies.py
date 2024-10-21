import csv
import time
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

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL to scrape
# ar=['0','1','2','3',
# ar=['4','5','6',
# ar=['7','8','9',
ar=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
list_comp=[]
k=0
for i in ar:
    if k==0:
        cnt=67
    else:
        cnt=1
    url = f"https://www.tofler.in/browsecompanies/{i}/{cnt}"
    driver.get(url)
    company_data = []  # Store company names
    while True:
        # Wait for the table body to load
        try:
            t_body = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
            )

            # Find all <a> elements within the <tbody>
            td_elements = WebDriverWait(t_body, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
            )

            if not td_elements:  # If no <a> elements found, break the loop
                break

            # Extract names from <a> elements
            names = []
            for td in td_elements:
                name = td.text.strip()
                if name:
                    names.append(name)

            company_data.extend(names)  # Add names to the list

        # Try to click the "Next" button

            next_button = driver.find_element(By.XPATH, "//a[normalize-space()='Next']")
            cnt+=1
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
        except Exception as e:
            print("No more pages or an error occurred:", e)
            print(f"Letter=> {i} Pages=> {cnt}")
            k=1
            break
    #         Last fetched data is from Letter A Page= 66 please check once
    #          last written line 10835

    list_comp.extend(company_data)
    if len(company_data) == 0:
        break




# print(list_comp)




# Save the collected company names to a CSV file
with open('company_tofler_names.csv', 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # writer.writerow(['Company Name'])  # Write the header
    for name in list_comp:
        writer.writerow([name])  # Write each name as a new row

print(f"{len(list_comp)} company names have been saved to company_names.csv.")

# Close the WebDriver
driver.quit()
