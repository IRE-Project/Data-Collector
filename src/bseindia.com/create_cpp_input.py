"""@file
This file is responsible for creating a file that can act as input for similarity.cpp
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
        line = line.split(",")
        if ret[line[0]] == []:
            ret[line[0]] = line
        else:
            if ret[line[0]] == line:
                print("Duplicate Data. Counted Only once", line[0])
            else:
                print("Security Codes are not unique", line[0])

    return ret


def load_cdata(file_path):
    """
    Loads json data from file_path
    :param file_path: path to json file
    :return: json parsed data
    """
    file = open(file_path, 'r')
    data = json.load(file)
    file.close()
    return data


def normalize(name):
    """
    normalizes the name of the company for comparison by lowercasing, substitution
    :param name: the name string
    :return: normalized string
    """
    if name == "-":
        return "company_name_not_available"
    name = name.lower().strip().replace("co ", "company").replace("co.", "company").replace("&", "and")
    name = name.lower().strip().replace("inc ", "incorporated").replace("inc.", "incorporated")
    name = ''.join(e for e in name if e.isalnum()).replace("ltd", "limited")
    return name


def create_cpp_input(bse, c_data, file_path):
    """
    Create the input file to act as input for similarity.cpp
    :param bse: the raw bse json data
    :param c_data: the links list exhaustive data
    :param file_path: the path to file that will act as input for similarity.cpp
    :return: None
    """
    file = open(file_path, "w+")
    file.write(str(len(bse)) + "\n")
    for key, val in bse.items():
        file.write(key + "\n")
        file.write(normalize(val[1]) + "\n")

    file.write(str(len(c_data)) + "\n")
    for key, val in c_data.items():
        file.write(key + "\n")
        file.write(normalize(val["Company"]) + "\n")
    file.close()


if __name__ == '__main__':
    nse_json = csv_to_json("../../data/bseindia.com/Select.csv")
    c_data = load_cdata('../../data/zaubacorp.com/links.json')
    create_cpp_input(nse_json, c_data, "inp.txt")
