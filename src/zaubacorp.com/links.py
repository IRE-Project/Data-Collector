"""@file
This file is responsible scraping the company information from zaubacorp listings to generate the base dataset.
"""
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json

links = defaultdict(lambda: {})
pages = 4687
total_items = 140581
items_per_page = 30


for page in range(1, pages + 1):

    try:
        item_count = 0
        source = requests.get(f"https://www.zaubacorp.com/company-list/roc-RoC-Hyderabad/p-{page}-company.html").text
        soup = BeautifulSoup(source, "lxml")

        table = soup.find('table', id='table')

        for row in table.find_all('tr'):
            row_elements = [col.text for col in row.find_all('td')]
            if row_elements:
                link = row.find('a')['href']

                if links[row_elements[0]] != {}:
                    print("INTEGRITY ERROR")
                    print(row_elements)
                    print(links[row_elements[0]])

                else:
                    links[row_elements[0]] = {
                        "Company": row_elements[1],
                        "RoC": row_elements[2],
                        "Status": row_elements[3],
                        "link": link
                    }
                    item_count += 1

        if item_count != items_per_page:
            print(f"NOT ALL ITEMS EXTRACTED ON PAGE {page}")

    except Exception as e:
        print("ERROR: ", str(e))
        print(page)


print("Items extracted:", len(links))
print("All items extracted: ", len(links) == total_items)

print("Dumping Data..")
file = open("../../data/zaubacorp.com/links.json", "w+")
json.dump(links, file, indent=4)
file.close()

print("data dumped in data/zaubacorp.com/links.json")
