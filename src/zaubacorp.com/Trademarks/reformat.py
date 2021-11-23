"""@file
This file is responsible for reformatting the zubacorp companies data such that it is ready for integration.
"""
import json


def reformat_trademarks(data):
    """
    Reformats the trademarks data to global standard.
    :param data: unformatted data
    :return: Formatted data
    """
    for key,val in data.items():
        if val == ["-"]:
            new_val = []
        else:
            new_val = [{
                "Name": ele[0],
                "Class": ele[1],
                "Class Description": ele[2],
                "Application Date": ele[3],
                "Status": ele[4],
                "Goods and Services Description": ele[5],
                "Applicant Address": ele[6],
                "Trademark Image": ele[7] if ele[7] != "-" else ""
            } for ele in val]

        data[key] = {
            "Trademarks": new_val
        }

    return data


if __name__ == "__main__":
    file = open("../../../data/zaubacorp.com/Trademarks/trademarks_cleaned.json")
    data = json.load(file)
    file.close()

    data = reformat_trademarks(data)

    file = open("../../../data/zaubacorp.com/Trademarks/trademarks_reformat.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
