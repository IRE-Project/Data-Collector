"""@file
This file is responsible for extracting website from google search results and formatting them for later use.
"""
import json
from urllib.parse import urlparse
import nltk
import os
tc = 0
cp = 0


def find_website(raw_data):
    """
    Uses several rule based techniques to find candidate websites for a company
    :param raw_data:
    :return: list of candidate websites
    """
    if raw_data["context"] != []:
        print(raw_data["context"])

    website = set()
    removed_tokens = ["ltd", "ltd.", "co", "co.", "limited", "services", "private", "govt", "government", "industries"
                      ,"incorporation", "public", "pvt", "and", "&"]
    c_name = [tok for tok in raw_data["query"].lower().strip().split() if tok not in removed_tokens]

    for ele in raw_data["top_urls"]:
        try:
            domain = urlparse(ele["url"]).netloc
            if "official" in ele["description"] and "website" in ele["description"]:
                website.add(domain)
            else:
                abbreviation = "".join([tok[0] for tok in c_name])
                webname = domain.split(".")
                if len(webname) < 2:
                    continue
                elif len(webname) == 2:
                    webname = webname[0]
                else:
                    if webname[1] == "co":
                        webname = webname[0]
                    else:
                        webname = webname[1]

                if nltk.edit_distance(webname, abbreviation) <= 2:
                    website.add(domain)

                elif any((tok in domain) and (len(tok) > 4) for tok in c_name):
                    website.add(domain)

        except Exception as e:
            print(str(e), ele)

    if len(website) > 0:
        global tc, cp
        cp += 1
        tc += len(website)

    # if len(website) > 1:
    #     print(c_name, website)

    return list(website)


def get_websites(raw):
    """
    get all candidate websites for all search results in raw
    :param raw: google search results
    :return: dict with company name and candidate websites
    """
    count = 0

    data = {}
    for key,val in raw.items():
        data[key] = {
            "Company": val["query"],
            "website": find_website(val)
        }
        count += 1
        print(f"\rProgress: {count}", end="")
    return data


def reformat(data, links):
    """
    Reformat data to better suit the global data paradigm
    :param data: unformatted data
    :param links: the exhaustive linkslist used
    :return: the formatted data
    """
    rev_map = {}
    for ele in links["data"]:
        rev_map[ele[1].lower().strip()] = ele[0]

    new_data = {}
    for key, val in data.items():
        cin = rev_map[val["Company"].lower().strip()]
        new_data[cin] = val["website"]
    print(len(new_data))
    return new_data


def get_all_websites(dir_path):
    """
    Get all websites for all files in a directory
    :param dir_path: path to directory
    :return: dict of unformatted comany names and candidate websites
    """
    data = {}
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".json") and file_name != "final_data.json":
            file = open(dir_path + file_name)
            raw = json.load(file)
            file.close()
            websites = get_websites(raw)

            for key, val in websites.items():
                data[key] = val
    return data


if __name__ == "__main__":
    data = get_all_websites("../../data/google.com/")
    print("\n", cp, tc)

    file = open("../../data/zaubacorp.com/linkslist.json")
    links = json.load(file)
    file.close()

    data = reformat(data, links)

    file = open("../../data/google.com/final_data.json", "w+")
    json.dump(data, file, indent=4)
    file.close()




