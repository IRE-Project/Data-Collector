"""@file
This file is responsible for reformatting the nse data such that it is ready for integration.
"""
import json


def reformat_nse(data):
    """
    Reformats the nse data to global standard
    :param data: unformatted data
    :return: Formatted data
    """
    for key,val in data.items():
        data[key] = {
            "NSE": val
        }
    return data


if __name__ == "__main__":
    file = open("../../data/nseindia.com/final_data.json")
    data = json.load(file)
    file.close()

    data = reformat_nse(data)

    file = open("../../data/nseindia.com/nse_reformat.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
