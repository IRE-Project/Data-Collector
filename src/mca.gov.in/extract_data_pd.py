"""@file
This file is responsible for extracting data from excel files into json files.
"""
import json
import pandas as pd
import os
from collections import defaultdict
import sys


def extract_data(path, json_path):
    """
    takes all the excel files in directory path and extracts the data in dict format
    whcih is finally stored in json_path
    :param path: path to directory
    :param json_path: final json output path
    :return: None
    """
    data = defaultdict(lambda : {})
    count = 0
    sys.stderr.write(str(count) + "\n")

    for file in os.listdir(path):
        sys.stderr.write(f"\r{count}")
        count += 1


        df = pd.read_excel(path+file)
        top_tag = "Company Master Data"
        
        CIN = file.split(".")[0]
        if "-" in CIN:
            top_tag = "LLP Master Data"
            
        if CIN != df.at[0, "Unnamed: 2"]:
            print("Integrity Error: File Integrity ", file)
        elif data[CIN] != {}:
            print("Integrity Error: Duplicate ", file)
        else:
            record = {}
            row = 0
            while True:
                key = df.at[row, top_tag]
                val = df.at[row, 'Unnamed: 2']
                row += 1
                if pd.isna(key):
                    break
                else:
                    record[key] = val


            row += 2
            charges = []
            if df.at[row, top_tag] != "No Charges Exists for Company/LLP":
                while True:
                    charge = [
                        df.at[row, top_tag],
                        df.at[row, 'Unnamed: 1'],
                        df.at[row, 'Unnamed: 2'],
                        df.at[row, 'Unnamed: 3'],
                        df.at[row, 'Unnamed: 4']
                    ]
                    row += 1
                    if pd.isnull(charge).all():
                        break
                    else:
                        charges.append(charge)
            else:
                row += 2
            record["Charges"] = charges

            row +=2
            directors = []
            if df.at[row, top_tag] != "No Signatory Exists for Company/LLP":
                while True and row < df.shape[0]:
                    director = [
                        df.at[row, top_tag],
                        df.at[row, 'Unnamed: 1'],
                        df.at[row, 'Unnamed: 2'],
                        df.at[row, 'Unnamed: 3']
                    ]
                    row += 1
                    if pd.isnull(director).all():
                        break
                    else:
                        directors.append(director)
            record["Directors/Signatory Details"] = directors

            data[CIN] = record


    file = open(json_path, "w+")
    json.dump(data, file, indent=4)
    file.close()


if __name__=="__main__":
    path = "../../data/mca.gov.in/mca_Data(125k)/V1/"
    json_path = "../../data/mca.gov.in/mca_Data(125k)/V1_extracted.json"
    extract_data(path, json_path)

    print()
    print("Next Version")

    path = "../../data/mca.gov.in/mca_Data(125k)/V2/"
    json_path = "../../data/mca.gov.in/mca_Data(125k)/V2_extracted.json"
    extract_data(path, json_path)

    print()
    print("Next Version")

    path = "../../data/mca.gov.in/mca_Data(125k)/V3/"
    json_path = "../../data/mca.gov.in/mca_Data(125k)/V3_extracted.json"
    extract_data(path, json_path)

# V1 18332
# V2 47117
# V3 59723