"""@file
This file is responsible for resolving all errors and integrity issues in trademarks and create the final
dataset for trademarks.
"""
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import re

digit_match = re.compile(r"[0-9]+")
comp_count = 0


def add_trademarks(trademarks, cin, c_name):
    """
    Finds all trademarks for the company denoted by cin,c_name and adds this to trademarks.
    If trademarks span multiple pages, it goes though them.
    :param trademarks: dict holding the trademarks data
    :param cin: CIN/LLPIN of the company
    :param c_name: Company name
    :return: None
    """
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


def find_missing():
    """
    Adds all the missing trademark values to trademark
    :return:
    """
    trademarks = defaultdict(lambda: [])
    missing_list = [
        ["U72200TG2013PTC088972", "TALIS IT SOLUTIONS PRIVATE LIMITED"],
        ["U65993TG1991PTC012660", "SOMSONS FINANCE AND INVESTMENTS PRIVATE LMITED"],
        ["U65910TG1995PLC020001", "SONA FINANCIAL SERVICES LTD"],
        ["U72200TG2013PTC089391", "VENMAH TECH SOLUTIONS PRIVATE LIMITED"],
        ["U01113TG2016PTC109214", "HIGHGROW CROP CARE PRIVATE LIMITED"],
        ["L74300TG1992PLC014317", "GRADIENTE INFOTAINMENT LIMITED"],
        ["U14107TG2008PTC060385", "GRANITECH MINERALS & CEMENTS PRIVATE LIMITED"],
        ["U14102TG1985PTC006002", "GRANITES AND TOOLS PVT LTD"],
        ["U74999TG2017OPC117558", "AVTES(OPC) PRIVATE LIMITED"],
        ["U74999TG2016PTC112480", "KETTE ENTERPRISES PRIVATE LIMITED"],
        ["U74110TG1996PLC024363", "NWONDER TRADERS LIMITED"],
        ["U72900TG2020PTC141495", "ITGEN INFO SYSTEMS PRIVATE LIMITED"],
        ["U01110TG2017PTC116834", "KIDDOGARDENER PRIVATE LIMITED"],
        ["AAQ-0160", "PABUJI PLYWOOD AND HARDWARE LLP"],
        ["U72900TG2017PTC114587", "GIGGS INNOVATIONS PRIVATE LIMITED"],
        ["U74999TG2011PTC076420", "GLITZ ANTIQUES & HERBS PRIVATE LIMITED"]
    ]
    print(len(missing_list))

    for ele in missing_list:
        print(ele)
        add_trademarks(trademarks, ele[0], ele[1])

    file = open(f"../../../data/zaubacorp.com/Trademarks/trademarks_missing.json", "w+")
    json.dump(trademarks,file, indent=4)
    file.close()


def accumulate_all():
    """
    Combines all the json files in trademark directory and and saves them in
    trademarks_final.json
    :return: None
    """
    final_data = {}
    path = "../../../data/zaubacorp.com/Trademarks/"
    for file_name in os.listdir(path):
        file = open(path + file_name, "r")
        trademarks = json.load(file)
        file.close()
        for key, val in trademarks.items():
            final_data[key] = val

    print(f"Done for {len(final_data)} CINs")
    file = open(f"../../../data/zaubacorp.com/Trademarks/trademarks_final.json", "w+")
    json.dump(final_data, file, indent=4)
    file.close()


if __name__ == "__main__":
    # find_missing()
    accumulate_all()