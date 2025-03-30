import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from time import sleep

def scrape_yc_startups(filename="", filetype="csv"):
    # Set up Chrome options (headless for non-GUI mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.ycombinator.com/companies/")

    # create an explicit wait
    wait = WebDriverWait(driver, 30)

    # wait for the first company to appear
    first_company = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a._company_i9oky_355")))
    old_company_text = first_company.text

    print("Companies loaded")

    # sort by launch date
    sort_select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select")))
    sort_select = Select(sort_select_element)

    sort_select.select_by_value("YCCompany_By_Launch_Date_production")

    # wait until the first company element from before is no longer attached to the DOM
    wait.until(EC.staleness_of(first_company))

    # wait for the first company in sorted list to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a._company_i9oky_355")))

    # Make sure the first company element’s text changes
    wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "a._company_i9oky_355").text != old_company_text)

    print("Sorted by launch date")

    # Initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    count = 0
    while True and count < 100:
        count += 1
        
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        sleep(2)  # Adjust the sleep duration as needed
        
        # Calculate new scroll height and compare with the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # If the scroll height hasn't changed, we've reached the bottom
        if new_height == last_height:
            print("✅ Reached the bottom of the page.")
            break
        last_height = new_height

    # now get updated page source
    html = driver.page_source
    driver.quit()

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    companies = soup.find_all("a", class_="_company_i9oky_355")
    print(f"Found {len(companies)} companies.")

    startups = []
    for comp in companies:
        # extract details from the company listing
        name = comp.find("span", class_="_coName_i9oky_470")
        location = comp.find("span", class_="_coLocation_i9oky_486")
        description = comp.find("span", class_="_coDescription_i9oky_495")
        
        startup = {
            "name": name.text.strip() if name.text else "N/A",
            "location": location.text.strip() if location.text else "N/A",
            "description": description.text.strip() if description.text else "N/A"
        }
        
        startups.append(startup)
    
    if filename:
        if filetype == "csv":
            # save to csv
            csv_columns = ["name", "location", "description"]
            with open("data/raw/yc_startups.csv", "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerows(startups)
        elif filetype == "json":
            # save to json
            with open("data/raw/yc_startups.json", "w", encoding="utf-8") as json_file:
                json.dump(startups, json_file, indent=4)
        else:
            raise ValueError("filetype must be \"csv\" or \"json\"")

        print("✅ Data saved successfully!")

    return startups
    
