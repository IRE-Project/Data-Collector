import json
import requests
from bs4 import BeautifulSoup
from collections import defaultdict


def check_log():
    log_file = open("../../data/zaubacorp.com/links_log.txt")

    while True:
        line = log_file.readline()

        if line == "":
            break
        elif line == "INTEGRITY ERROR\n":
            try:
                new_data = [ele.strip("\'") for ele in log_file.readline().strip('\n][').split(", ")]
                old_data = json.loads(log_file.readline().replace("\'", '\"'))

                if new_data[1] == old_data["Company"] and new_data[2] == old_data["RoC"] and new_data[3] == old_data[
                    "Status"]:
                    pass
                else:
                    print(new_data)
                    print(old_data)

            except Exception as e:
                print(new_data)

        else:
            print(line)


def include_missing(links, page):
    print("PAGE: ", page)
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
                    pass

                else:
                    print(row_elements, link)
                    links[row_elements[0]] = {
                        "Company": row_elements[1],
                        "RoC": row_elements[2],
                        "Status": row_elements[3],
                        "link": link
                    }
                    item_count += 1

        print("Items Extracted: ", item_count)
        print()

    except Exception as e:
        print("ERROR: ", str(e))
        print(page)


def verify(links):
    ret = True
    for key, val in links.items():
        if len(key) < 2 or len(val["Company"]) < 2 or len(val["RoC"]) < 2 or len(val["Status"]) < 2 or len(
                val["link"]) < 2:
            print(key, val)
            ret = False

    return ret


# check_log()

file = open("../../data/zaubacorp.com/links.json", "r")
links = defaultdict(dict, json.load(file))
file.close()

for page in range(1705, 1716):
    include_missing(links, page)

print("Verify: ", verify(links))

print(len(links))

file = open("../../data/zaubacorp.com/links.json", "w+")
json.dump(links, file, indent=4)
file.close()
