"""@file
This file is responsible for parsing the c++ output.
"""
import json
from collections import defaultdict


def csv_to_json(file_path):
    """
    Format the csv data to dict format
    :param file_path: path to csv
    :return: dict formatted csv data
    """
    file = open(file_path)
    file.readline()
    ret = defaultdict(lambda: [])
    while True:
        line = file.readline()
        if line == "":
            break
        line = [ele for ele in line.strip().split(",") if ele != ""]
        if ret[line[0]] == []:
            ret[line[0]] = line
        else:
            if ret[line[0]] == line:
                print("Duplicate Data. Counted Only once", line[0])
            else:
                print("Security Codes are not unique", line[0])

    return ret


def parse_output(file_path):
    """
    Parse the c++ output and extract information in dict format
    :param file_path: path to c++ out file
    :return: extracted data in dict format
    """
    file = open(file_path)
    count = 0
    cp = 0
    tc = 0
    output = {}
    while True:
        line = file.readline()
        if line == "":
            break
        cin = line.rstrip("\n")
        c_name = file.readline().rstrip("\n")
        candidates = []

        while True:
            code = file.readline().rstrip("\n")
            if code == "--DONE--":
                break
            name = file.readline().rstrip("\n")
            candidates.append([code, name])

        output[cin] = {
            "c_name": c_name,
            "candidates": candidates
        }
        count += 1
        print(f"\rProgress = {count}", end="")
        if candidates != []:
            cp += 1
            tc += len(candidates)


    print(f"\nCINs parsed = {count}")
    print(cp, tc)
    return output



def create_final_dataset(raw_data, out, file_path):
    """
    Formats the parsed data ofr further use.
    :param raw_data: the bse raw data from csv file
    :param out: the parsed c++ output
    :param file_path: path where the data will be saved
    :return: None
    """
    data = {}
    count = 0
    for key, val in out.items():
        item = []
        if len(val["candidates"]) > 0:
            for ele in val["candidates"]:
                item.append(raw_data[ele[0]])

        data[key] = item
        count += 1
        print(f"\rProgress = {count}", end="")

    file = open(file_path, "w+")
    json.dump(data, file, indent=4)
    file.close()


if __name__ == "__main__":
    output = parse_output("out2.txt")
    bse_raw = csv_to_json("../../data/bseindia.com/Select.csv")
    create_final_dataset(bse_raw, output, "../../data/bseindia.com/final_data.json")

# 187 537
# 455 954
