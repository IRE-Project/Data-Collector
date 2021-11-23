"""@file
This file is responsible for cleaning up the bse data.
"""

import json


def cleanup(data):
    """
    Cleans up the data by removing whitespaces.
    :param data:
    :return:
    """
    for key, val in data.items():
        new_val = []
        for ele in val:
            item = [tok.strip() for tok in ele]
            item = [tok for tok in item if tok != "\""]
            item = [tok.replace("\"", "") for tok in item]
            new_val.append(item)
        data[key] = new_val
    return data


def verify(data):
    """
    Checks if all the urls in data are valid or not
    :param data:
    :return: None
    """
    for key,val in data.items():
        if any([len(ele) != 10 for ele in val]):
            print("Length Error")
            print(key, val)
            print([len(ele) != 10 for ele in val])


if __name__ == "__main__":
    file = open("../../data/bseindia.com/final_data.json")
    data = json.load(file)
    file.close()

    data = cleanup(data)
    verify(data)

    file = open("../../data/bseindia.com/bse_cleaned.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
# 523455