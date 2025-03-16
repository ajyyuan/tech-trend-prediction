from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

print(first_company, old_company_text)

# sort by launch date
sort_select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select")))
sort_select = Select(sort_select_element)

sort_select.select_by_value("YCCompany_By_Launch_Date_production")

# wait until the first company element from before is no longer attached to the DOM
print("First company is attached to the DOM.")

wait.until(EC.staleness_of(first_company))
print("First company is no longer attached to the DOM.")
print(first_company)

# wait for the first company in sorted list to appear
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a._company_i9oky_355")))

# Make sure the first company element’s text changes
wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "a._company_i9oky_355").text != old_company_text)


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
    
    print("Name:", startup["name"])
    print("Location:", startup["location"])
    print("Description:", startup["description"])
    print("-" * 40)
    
    startups.append(startup)
