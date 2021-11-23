"""@file
This file is responsible for reformatting the zubacorp companies data such that it is ready for integration.
"""
import json


def reformat_companies(data):
    """
    Reformats the zaubacorp data to global standard by renaming. Also removes some unneeded columns.
    :param data: unformatted data
    :return: Formatted data
    """
    for key, val in data.items():
        val["Prosecutions"] = val["Persecution"]
        del val["Persecution"]

        val["Previous CINs"] = val["Previous CIN"]
        del val["Previous CIN"]

        del val["total Charges/Borrowing Amount"]
        del val['Number of Persecutions']
        del val['Number of Charges']

        val['Authorised Capital'] = val['Authorised Capital'].replace("\u20b9", "")
        val['Paid up capital'] = val['Paid up capital'].replace("\u20b9", "")
        val["Total Obligation of Contribution"] = val["Total Obligation of Contribution"].replace("\u20b9", "")

        if val["Activity"] != "" and (val['Description of main division'] != "" or val["Main division of business activity to be carried out in India"] != ""):
            print("Both in val", key)

        if val["Activity"] == "":
            if val['Description of main division'] != val["Main division of business activity to be carried out in India"]:
                print("Not same act description")
            val["Activity"] = val["Main division of business activity to be carried out in India"]

        del val['Description of main division']
        del val["Main division of business activity to be carried out in India"]

        data[key] = val
    return data


if __name__ == "__main__":
    file = open("../../../data/zaubacorp.com/Companies/Companies_cleaned.json")
    data = json.load(file)
    file.close()

    data = reformat_companies(data)
    print(len(data))

    file = open("../../../data/zaubacorp.com/Companies/Companies_reformat.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
