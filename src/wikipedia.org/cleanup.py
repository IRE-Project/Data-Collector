"""@file
This file is responsible for cleaning up the wikipedia data.
"""
import json


def cleanup(data):
    """
    Cleans up the data by removing unicode symbols and invalid websites
    :param data:
    :return: cleaned data
    """
    for key, val in data.items():
        to_del_Web = False
        for col, col_val in val.items():
            if col == "website":
                if "." not in col_val:
                    to_del_Web = True
            elif type(col_val) == str:
                val[col] = col_val.strip().replace("\u20b9", "").replace("\u00a0", "")
        if to_del_Web:
            del val["website"]
        data[key] = val
    return data


if __name__ == "__main__":
    file = open("../../data/wikipedia.org/wikidata_cleaned.json")
    data = json.load(file)
    file.close()

    data = cleanup(data)

    file = open("../../data/wikipedia.org/wikidata_final.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
