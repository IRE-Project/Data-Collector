"""@file
This file is responsible for cleaning up the mca.gov.in data. Commented out in the end is
the list of columns extracted.
"""
import json
import os
import math

def combine(dir_path, json_path):
    """
    Combines the json files in dir_path and saves them in json_path
    :param dir_path: path to directory with all json run files
    :param json_path: the final output path where the combined json file will be stored
    :return: the combined json file
    """
    combined_data = {}
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".json"):
            file = open(dir_path + file_name)
            data = json.load(file)
            file.close()

            for key,val in data.items():
                combined_data[key] = val

    print(f"CINs collected: {len(combined_data)}")

    file = open(json_path, "w+")
    json.dump(combined_data, file, indent=4)
    file.close()

    return combined_data


def create_missing_list(data):
    """
    Creates a list of missing companies that are not in data
    :param data:
    :return: None
    """
    file = open("../../data/zaubacorp.com/links.json")
    links = json.load(file)
    file.close()

    missing = {}

    for key, val in links.items():
        if key not in data or data[key] == None:
            missing[key] = val

    file = open("../../data/zaubacorp.com/missing_links.json", "w+")
    json.dump(missing, file, indent=4)
    file.close()


def create_col_list(data):
    """
    Iterates over all data to get the list of columns in the dataset
    :param data:
    :return: set of columns
    """
    columns = set()
    for key,val in data.items():
        try:
            for col in val.keys():
                columns.add(col)
        except Exception as e:
            print(key)
    return columns


def replace_nan_trim(data):
    """
    Cleans up the dataset and makes it more standard by replacing NaN by "" and
    trimming the strings
    :param data:
    :return: the cleaned up data
    """
    for key, val in data.items():
        for col, col_val in val.items():
            if type(col_val) == float and math.isnan(col_val):
                val[col] = ""
            elif type(col_val) == str:
                val[col] = col_val.strip()
            elif col in ["Charges", 'Directors/Signatory Details']:
                new_list = []
                for ele in col_val:
                    new_ele = []
                    for item in ele:
                        if type(item) == float and math.isnan(item):
                            new_ele.append("")
                        elif type(item) == str:
                            new_ele.append(item.strip())
                        else:
                            new_ele.append(item)
                    new_list.append(new_ele)
                val[col] = new_list

        data[key] = val
    return data


def fill_empty_cols(data, columns):
    """
    Creates key, value pair with null values for the columns not present.
    :param data:
    :param columns: set of columns in data
    :return: the updated data
    """
    for key, val in data.items():
        for col in columns:
            if col not in val:
                if col in ["Charges", 'Directors/Signatory Details']:
                    val[col] = []
                else:
                    val[col] = ""
        data[key] = val
    return data


def normalize_date(date_string):
    """
    Converts string to DD-MM-YYYY form
    :param date_string: string to be converted
    :return: normalized string
    """
    if date_string in ["", "-"]:
        return ""
    normalized_date = date_string.split("/")
    return "-".join(normalized_date)


def reformat_dates(data):
    """
    Finds all dates present in data and reformats them to DD-MM-YYYY form.
    :param data:
    :return: the updated data
    """
    for key, val in data.items():
        for col, col_val in val.items():
            if col in ["Date of last AGM", 'Date of Incorporation',
                       'Date of last financial year end date for which Statement of Accounts and Solvency filed',
                       'Date of Balance Sheet', 'Date of last financial year end date for which Annual Return filed']\
                    and col_val != "":
                val[col] = normalize_date(col_val)
            elif col == "Charges":
                new_list = []
                for ele in col_val:
                    new_list.append([ele[0], ele[1], normalize_date(ele[2]), normalize_date(ele[3]), ele[4]])
                val[col] = new_list
            elif col == 'Directors/Signatory Details':
                new_list = []
                for ele in col_val:
                    new_list.append([ele[0], ele[1], normalize_date(ele[2]), normalize_date(ele[3])])
                val[col] = new_list

        data[key] = val
    return data


if __name__ == "__main__":
    # data = combine("../../data/mca.gov.in/mca_Data(125k)/", "../../data/mca.gov.in/mca_Data(125k)/mca_final.json")

    file = open("../../data/mca.gov.in/mca_Data(125k)/mca_final.json")
    data = json.load(file)
    file.close()

    columns = create_col_list(data)
    data = replace_nan_trim(data)
    data = fill_empty_cols(data ,columns)
    data = reformat_dates(data)

    file = open("../../data/mca.gov.in/mca_Data(125k)/mca_cleaned.json", "w+")
    json.dump(data, file, indent=4)
    file.close()

#{'Company / LLP Name', 'Company Name'
# 'Paid up Capital(Rs)', 'Paid up capital'
# 'Date of last AGM', 'Date of Last Annual General Meeting'
# 'Date of Incorporation',
# 'Authorised Capital(Rs)', 'Authorised Capital'
# 'Company Category',
# 'LLP Name', 'Company Name'
# 'Number of Partners', 'Number Of Partners'
# 'LLPIN', - del
# 'Date of last financial year end date for which Statement of Accounts and Solvency filed',
# 'CIN', - del
# 'Email Id', 'Email'
# 'Registration Number',
# 'Company SubCategory', 'Company Sub Category'
# 'Number of Designated Partners',
# 'Charges',
# 'Total Obligation of Contribution',
# 'Registered Address', 'Address'
# 'Whether Listed or not', 'Listing Status'
# 'Directors/Signatory Details', 'Current Directors'
# 'Main division of business activity to be carried out in India ',
# 'ROC Code', 'RoC'
# 'Description of main division',
# 'Class of Company ','Class of Company'
# 'Previous firm/ company details,if applicable', -del
# 'Date of Balance Sheet', 'Date of Latest Balance Sheet'
# 'Number of Members(Applicable in case of company without Share Capital)', 'Number of Members'
# 'Company Status(for efiling)', 'Company Status'
# 'LLP Status', 'Company Status'
# 'Date of last financial year end date for which Annual Return filed'}
