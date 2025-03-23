import json
import csv
from yc_scraper import scrape_yc_startups

startups = scrape_yc_startups()

# save to json
with open("data/raw/yc_startups.json", "w", encoding="utf-8") as json_file:
    json.dump(startups, json_file, indent=4)

# save to csv
csv_columns = ["name", "location", "description"]
with open("data/raw/yc_startups.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(startups)

print("✅ Data saved successfully!")
