"""@file
This file is responsible for reformatting the mca.gov.in data such that it is ready for integration.
"""
import json


def reformat_companies(data):
    """
    Reformats the mca.gov.in data to global standard by renaming and restructuring. Also removes some unneeded columns
    :param data: unformatted data
    :return: Formatted data
    """
    rename = [

        ['Paid up Capital(Rs)', 'Paid up capital'],
        ['Date of last AGM', 'Date of Last Annual General Meeting'],
        ['Authorised Capital(Rs)', 'Authorised Capital'],
        ['Email Id', 'Email'],
        ['Company SubCategory', 'Company Sub Category'],
        ['Registered Address', 'Address'],
        ['Whether Listed or not', 'Listing Status'],
        ['Directors/Signatory Details', 'Current Directors'],
        ['ROC Code', 'RoC'],
        ['Date of Balance Sheet', 'Date of Latest Balance Sheet'],
        ['Number of Members(Applicable in case of company without Share Capital)', 'Number of Members'],
        ['Class of Company ','Class of Company']
        ]

    deletions = ['LLPIN', 'CIN', "Previous firm/ company details, if applicable", 'Description of main division', 'Main division of business activity to be carried out in India ',
                 'Company / LLP Name', 'LLP Name', 'Company Status(for efiling)', 'LLP Status', 'Number of Designated Partners',
                 'Number of Partners', 'Date of last financial year end date for which Annual Return filed', 'Date of last financial year end date for which Statement of Accounts and Solvency filed']
    for key, val in data.items():
        for ele in rename:
            before, after = ele
            val[after] = val[before]
            del val[before]

        val["Activity"] = val['Description of main division']
        val['Company Name'] = val['Company / LLP Name'] if val['Company / LLP Name'] != "" else val['LLP Name']
        val['Company Status'] = val['Company Status(for efiling)'] if val['Company Status(for efiling)'] != "" else val['LLP Status']
        val['Number Of Partners'] = val['Number of Partners'] if val['Number of Partners'] != "" else val['Number of Designated Partners']

        for ele in deletions:
            del val[ele]

        data[key] = val
    return data


if __name__ == "__main__":
    file = open("../../data/mca.gov.in/mca_Data(125k)/mca_cleaned.json")
    data = json.load(file)
    file.close()

    data = reformat_companies(data)
    print(len(data))

    file = open("../../data/mca.gov.in/mca_Data(125k)/mca_reformat.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
