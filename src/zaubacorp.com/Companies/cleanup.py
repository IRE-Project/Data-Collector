"""@file
This file is responsible for cleaning up the company data from zaubacorp. Commented out in the end is
the list of columns extracted.
"""

import json
import os
import nltk

month_dict = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}


def combine(dir_path, json_path):
    """
    Combines the json files in dir_path and saves them in json_path
    :param dir_path: path to directory with all json run files
    :param json_path: the final output path where the combined json file will be stored
    :return: the combined json file
    """
    combined_data = {}
    for file_name in os.listdir(dir_path):
        if file_name in ["Companies_cleaned.json", "Companies_final.json", "Companies_reformat.json"]:
            continue
        file = open(dir_path + file_name)
        data = json.load(file)
        file.close()

        for key,val in data.items():
            if val is not None:
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
    file = open("../../../data/zaubacorp.com/links.json")
    links = json.load(file)
    file.close()

    missing = {}

    for key, val in links.items():
        if key not in data or data[key] == None:
            missing[key] = val

    file = open("../../../data/zaubacorp.com/missing_links.json", "w+")
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


def remove_nulls(data):
    """
    Removes those key value pairs from data where value is None
    :param data:
    :return: the cleaned up data
    """
    null_keys = []
    for key, val in data.items():
        if val == None:
            null_keys.append(key)
    for key in null_keys:
        del data[key]

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
                if col == "Previous CIN" or col == "Previous Names":
                    val[col] = []
                elif col in ["Current Directors", "Charges" , "Establishments", "Persecution"]:
                    val[col] = {}
                else:
                    val[col] = ""

            elif col == "Current Directors":
                col_val = val[col]
                for i_key, i_val in col_val.items():
                    for d_key in ["Name", "Designation", "Appointment Date"]:
                        if d_key not in i_val:
                            i_val[d_key] = ""
                    col_val[i_key] = i_val
                val[col] = col_val

            elif col == "Charges":
                col_val = val[col]
                for i_key, i_val in col_val.items():
                    for d_key in ["Creation Date", "Modification Date", "Closure Date", "Assets Under Charge", "Amount", "Charge Holder"]:
                        if d_key not in i_val:
                            i_val[d_key] = ""
                    col_val[i_key] = i_val
                val[col] = col_val

            elif col == "Establishments":
                col_val = val[col]
                for i_key, i_val in col_val.items():
                    for d_key in ["Establishment Name", "City", "Pincode", "Address"]:
                        if d_key not in i_val:
                            i_val[d_key] = ""
                    col_val[i_key] = i_val
                val[col] = col_val

            elif col == "Persecution":
                col_val = val[col]
                for i_key, i_val in col_val.items():
                    for d_key in ["Defaulting Entities", "Court Name", "Prosecution Section", "Date Of Order", "Status"]:
                        if d_key not in i_val:
                            i_val[d_key] = ""
                    col_val[i_key] = i_val
                val[col] = col_val

        data[key] = val
    return data


def normalize_date(date_string):
    """
    Converts string to DD-MM-YYYY form
    :param date_string: string to be converted
    :return: normalized string
    """
    if any([month in date_string for month in month_dict.keys()]):
        normalized_date = date_string.split()
        normalized_date[1] = month_dict[normalized_date[1]]
        return "-".join(normalized_date)
    else:
        normalized_date = date_string.split("-")
        normalized_date.reverse()
        return "-".join(normalized_date)


def reformat_dates(data):
    """
    Finds all dates present in data and reformats them to DD-MM-YYYY form.
    :param data:
    :return: the updated data
    """
    for key, val in data.items():
        for col, col_val in val.items():
            if col in ['Date of Last Annual General Meeting', 'Date of Incorporation', 'Date of Latest Balance Sheet']\
                    and col_val != "":
                val[col] = normalize_date(col_val)
            elif col in ["Current Directors", "Charges","Persecution"]:
                try:
                    for i_key, i_val in col_val.items():
                        for ii_key, ii_val in i_val.items():
                            if "Date" in ii_key and ii_val != "":
                                i_val[ii_key] = normalize_date(ii_val)
                        col_val[i_key] = i_val
                    val[col] = col_val
                except Exception as e:
                    print()
                    print(col, col_val)
        data[key] = val
    return data


def compare_dict(dict1, dict2):
    """
    Compares dictionaries for similarity using edit distance
    :param dict1:
    :param dict2:
    :return: True if similarity score is high, False otherwise
    """
    for key in dict1.keys():
        if key in ["Establishment Name", "Address"]:
            if nltk.edit_distance(dict1[key], dict2[key]) > 2:
                return False
        elif dict1[key] != dict2[key]:
            return False
    return True


def remove_duplicates(data):
    """
    Removes dulicate entries in multivalued fields
    :param data:
    :return: the updated data
    """
    for key,val in data.items():
        for col in ["Establishments", "Persecution"]:
            new_val = []
            for ele in val[col].values():
                present = False
                for item in new_val:
                    if compare_dict(item, ele):
                        present = True
                        break
                if not present:
                    new_val.append(ele)
            val[col] = new_val
        data[key] = val
    return data


if __name__ == "__main__":
    # data = combine("../../../data/zaubacorp.com/Companies/", "../../../data/zaubacorp.com/Companies/Companies_final.json")

    file = open("../../../data/zaubacorp.com/Companies/Companies_final.json")
    data = json.load(file)
    file.close()

    # create_missing_list(data)
    columns = create_col_list(data)
    # print(columns)
    data = remove_nulls(data)
    data = fill_empty_cols(data, columns)
    data = reformat_dates(data)
    data = remove_duplicates(data)
    print(len(data))

    file = open("../../../data/zaubacorp.com/Companies/Companies_cleaned.json", "w+")
    json.dump(data, file, indent=4)
    file.close()


# {'Number of Members',
# 'Charges',
    # "90133437": {                 // Charge ID
    #     "Creation Date": "1988-05-03",
    #     "Modification Date": "1995-09-14",
    #     "Closure Date": "1998-01-02",
    #     "Assets Under Charge": "Immovable property or any interest therein; Movable property (not being pledge)",
    #     "Amount": 2500000,
    #     "Charge Holder": "PUNJAB NATIONAL BANK"

# 'Persecution',
#     "0": {
#         "Defaulting Entities": "1.M.P. Murthy2.N.R. Pinna3.P. Ramarao4.P. Geeta Rao",
#         "Court Name": "Special judge for economic offences court - Hyderabad",
#         "Prosecution Section": 63,
#         "Date Of Order": "24-02-2003",
#         "Status": "Finalization of Charge"
#     }

# 'Number of Designated Partners',
# 'Date of Latest Balance Sheet',
# 'Email',
# 'Description of main division',
# 'Number of Persecutions',
# 'Previous CIN',
# 'total Charges/Borrowing Amount',
# 'Main division of business activity to be carried out in India',
# 'RoC',
# 'Current Directors',
#     "02547629": {
#         "Name": "SUMEET CHAWLA",
#         "Designation": "Director",
#         "Appointment Date": "18 August 2017"

# 'Date of Incorporation',
# 'Number of Charges',
# 'Paid up capital',
# 'Number Of Partners',
# 'Previous Names',
# 'Number of Employees',
# 'Activity',
# 'Website',
# 'Address',
# 'Class of Company',
# 'Total Obligation of Contribution',
# 'Company Name',
# 'Date of Last Annual General Meeting',
# 'Authorised Capital',
# 'Company Status',
# 'Company Sub Category',
# 'Company Category',

# 'Establishments',
#     "Establishment Name": "KHAMMAM GRANITE PVT LTD.",
#     "City": "WARANGAL",
#     "Pincode": 507002,
#     "Address": "IDAKHANAPURAM HAVELIKHAMMAMKHAMMAM"

# 'Age of Company',
# 'Registration Number'}
