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
driver = webdriver.Chrome()

# URL to scrape
url = "https://www.tofler.in/browsecompanies/0/1"
driver.get(url)

company_data = []  # Store company names

while True:
    # Wait for the table body to load
    t_body = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
    )

    # Find all <a> elements within the <tbody>
    td_elements = WebDriverWait(t_body, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'a'))
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
    try:
        next_button = driver.find_element(By.XPATH, "//a[normalize-space()='Next']")
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    except Exception as e:
        print("No more pages or an error occurred:", e)
        break

# Save the collected company names to a CSV file
with open('company_names.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])  # Write the header
    for name in company_data:
        writer.writerow([name])  # Write each name as a new row

print(f"{len(company_data)} company names have been saved to company_names.csv.")

# Close the WebDriver
driver.quit()
