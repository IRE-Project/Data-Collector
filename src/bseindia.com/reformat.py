"""@file
This file is responsible for reformatting the bse data such that it is ready for integration.
"""
import json


def reformat_bse(data):
    """
    Reformats the bse data to global standard
    :param data: unformatted data
    :return: Formatted data
    """
    for key,val in data.items():
        new_val = [{
            "Security Code": int(ele[0]),
            "Security Id": ele[2],
            "Security Name": ele[3],
            "Status": ele[4],
            "Group": ele[5],
            "Face Value": float(ele[6]),
            "ISIN No": ele[7],
            "Industry": ele[8],
            "Instrument": ele[9]
        } for ele in val]

        data[key] = {
            "BSE": new_val
        }
    return data


if __name__ == "__main__":
    file = open("../../data/bseindia.com/bse_cleaned.json")
    data = json.load(file)
    file.close()

    data = reformat_bse(data)

    file = open("../../data/bseindia.com/bse_reformat.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
