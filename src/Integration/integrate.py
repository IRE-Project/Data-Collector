"""@file
This file is responsible for combining all the datsets and resolving their conflicts and merge them into one.
"""
import json


def combine(links, mca_data, zauba_data, trademarks_data, nse_data, bse_data, wiki_data, websites):
    """
    For each cin in links the function adds all the key value pairs in fixed priority order
    to resolve merge conflicts.
    :param links:
    :param mca_data:
    :param zauba_data:
    :param trademarks_data:
    :param nse_data:
    :param bse_data:
    :param wiki_data:
    :param websites:
    :return: the final dataset
    """
    final_data = {}
    for cin in links.keys():
        item = {}
        for key, val in nse_data[cin].items():
            item[key] = val
        for key, val in bse_data[cin].items():
            item[key] = val
        for key, val in trademarks_data[cin].items():
            item[key] = val

        for key, val in zauba_data[cin].items():
            item[key] = val

        if cin in mca_data:
            for key, val in mca_data[cin].items():
                if key in ["Charges", "Current Directors"]:
                    pass
                elif (key in item and val != "" and val != 0) or (key not in item):
                    item[key] = val

        item["Additional"] = {}
        if cin in wiki_data:
            for key, val in wiki_data[cin].items():
                if key == "website":
                    item["Website"] = val
                else:
                    item["Additional"][key] = val

        if cin in websites and item["Website"] == "":
            if websites[cin] != []:
                item["Additional"]["Possible Websites"] = websites[cin]

        final_data[cin] = item
    return final_data


if __name__ == "__main__":
    file = open("../../data/zaubacorp.com/links.json")
    links = json.load(file)
    file.close()

    file = open("../../data/mca.gov.in/mca_Data(125k)/mca_reformat.json")
    mca_data = json.load(file)
    file.close()

    file = open("../../data/zaubacorp.com/Companies/Companies_reformat.json")
    zauba_data = json.load(file)
    file.close()


    file = open("../../data/zaubacorp.com/Trademarks/trademarks_reformat.json")
    trademarks_data = json.load(file)
    file.close()

    file = open("../../data/nseindia.com/nse_reformat.json")
    nse_data = json.load(file)
    file.close()

    file = open("../../data/bseindia.com/bse_reformat.json")
    bse_data = json.load(file)
    file.close()

    file = open("../../data/wikipedia.org/wikidata_final.json")
    wiki_data = json.load(file)
    file.close()

    file = open("../../data/google.com/final_data.json")
    websites = json.load(file)
    file.close()

    final_data = combine(links, mca_data, zauba_data, trademarks_data, nse_data, bse_data, wiki_data, websites)
    print(len(final_data))

    file = open("../../data/integrated.json", "w+")
    json.dump(final_data, file, indent=4)
    file.close()