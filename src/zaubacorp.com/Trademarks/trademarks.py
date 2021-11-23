import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import re

digit_match = re.compile(r"[0-9]+")
comp_count = 0


def add_trademarks(trademarks, cin, c_name):

    page = 1
    c_tms = []
    record_count = 0
    item = 0
    global comp_count

    try:

        while True:
            response = requests.get(f"https://www.zaubacorp.com/company-trademark/{c_name}/{cin}/page-{page}")

            if response.status_code != 200:
                if page == 1:
                    raise Exception(response.status_code)
                else:
                    break

            soup = BeautifulSoup(response.text, "lxml")

            record = soup.find('div', class_="col-xs-4 text-left")
            if record:
                record_count = digit_match.findall(record.text)
                if record_count:
                    record_count = int(record_count[0])

            tm_records = soup.find_all('span', class_="wordMark")
            if tm_records:
                for i in range(0, len(tm_records), 3):
                    c_tms.append([tm_records[i].text.split(":")[1].strip(), tm_records[i + 1].text.split(":")[1].strip(), tm_records[i + 1].a["title"]])

                tm_labels = soup.find_all('div', class_="main-wrapper")

                for record in tm_labels:
                    elements = record.text.strip().split("\n")
                    for ele in elements:
                        c_tms[item].append(ele.split(":")[1].strip())
                    if record.img is not None:
                        c_tms[item].append(record.img['src'])
                    else:
                        c_tms[item].append("-")
                    item += 1

                page += 1
            else:
                break

        if trademarks[cin] != []:
            print("This is already present in trademarks: ", cin, c_name)
        else:
            if c_tms:
                trademarks[cin] = c_tms
                comp_count += 1
            else:
                trademarks[cin] = ["-"]

        if len(c_tms) != record_count:
            print("Not all records extracted", cin, c_name, len(c_tms))

    except Exception as e:
        print(str(e))
        print(cin, c_name)


file = open("../../data/zaubacorp.com/linkslist.json", "r")
links = json.load(file)
file.close()

trademarks = defaultdict(lambda: [])

start = int(input("Starting Index(Inclusive): "))
end = int(input("End Index(Inclusive): "))

k = 0
for row in links["data"][start: end+1]:
    add_trademarks(trademarks, row[0], row[1])
    k += 1
    print(f"\rProgress: {k} / {end - start + 1}", end="")

print("\n\nCompanies with at least 1 Trademark: ", comp_count)

file = open(f"../../data/zaubacorp.com/trademarks{start}-{end}.json", "w+")
json.dump(trademarks,file, indent=4)
file.close()
