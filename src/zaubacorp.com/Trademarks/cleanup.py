"""@file
This file is responsible for cleaning up the trademarks data by removing duplicates.
"""

import json
from urllib.parse import urlparse


def remove_duplicates(data):
    """
    Removes dulicate entries by considering first 7 of the list items as keys.
    :param data:
    :return: the updated data
    """
    duplicate_count = 0
    for key, val in data.items():
        if val != ["-"]:
            initial_length = len(val)
            new_val = list(set(["$^".join(ele[:7]) for ele in val]))
            for i in range(len(new_val)):
                for ele in val:
                    if new_val[i] == "$^".join(ele[:7]):
                        new_val[i] += "$^" + ele[7]
                        break

            data[key] = [ele.split("$^") for ele in new_val]

            if any([len(ele) != 8 for ele in data[key]]):
                print("\nLength Error", val)
                print(data[key])
                print([len(ele) != 8 for ele in data[key]])

            duplicate_count += initial_length - len(data[key])

    print(f"Duplicates Removed = {duplicate_count}")
    return data


def reformat_dates(data):
    """
    Reformats all dates present in data to DD-MM-YYYY form.
    :param data:
    :return: the updated data
    """
    for key, val in data.items():
        if val != ["-"]:
            for i in range(len(val)):
                date = val[i][3].split("-")
                date.reverse()
                val[i][3] = "-".join(date)

            data[key] = val

    return data


def is_url(url):
    """
    Checks validity of url
    :param url:
    :return: True if url is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def verify_links(data):
    """
    Verifies all the image links provided in trademarks
    :param data:
    :return: True if all links are valid, False otherwise
    """
    for key, val in data.items():
        if val != ["-"]:
            for i in range(len(val)):
                if val[i][7] == "-":
                    continue
                elif not is_url(val[i][7]):
                    print("Invalid Link")

    print("Links Validated")


if __name__ == "__main__":
    file = open("../../../data/zaubacorp.com/Trademarks/trademarks_final.json")
    data = json.load(file)
    file.close()

    data = reformat_dates(data)
    verify_links(data)
    data = remove_duplicates(data)

    file = open("../../../data/zaubacorp.com/Trademarks/trademarks_cleaned.json", "w+")
    json.dump(data, file, indent=4)
    file.close()
