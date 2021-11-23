"""@file
This file is responsible for parsing the c++ output.
"""
import json
import nltk


def parse_output(file_path):
    """
    Parse the c++ output and extract information in dict format
    :param file_path: path to c++ out file
    :return: extracted data in dict format
    """
    file = open(file_path)
    count = 0
    output = {}
    while True:
        line = file.readline()
        if line == "":
            break
        cin = line.rstrip("\n")
        c_name = file.readline().rstrip("\n")
        candidates = []

        while True:
            name = file.readline().rstrip("\n")
            if name == "--DONE--":
                break
            capital = float(file.readline().rstrip("\n"))
            symbol = file.readline().rstrip("\n")
            candidates.append([name, capital, symbol])

        output[cin] = {
            "c_name": c_name,
            "candidates": candidates
        }
        count += 1
        print(f"\rProgress = {count}", end="")

    print(f"\nCINs parsed = {count}")
    return output


def filter_output(output, filter_val):
    """
    Filters out the output with similarity score less than filter_val
    :param output: The parsed json output
    :param filter_val: similarity cut off
    :return: the updated output
    """
    new_output = {}
    count = 0
    for key, val in output.items():
        c_name = val["c_name"].replace("_", "")
        new_candidates = []
        for ele in val["candidates"]:
            name = ele[0].replace("_", "")
            ed = nltk.edit_distance(c_name.lower(), name.lower())
            similarity = 100 * (1 - ed / len(c_name))
            if similarity > filter_val:
                new_candidates.append(ele)

        new_output[key] = {
            "c_name": c_name,
            "candidates": new_candidates
        }
        count += 1
        print(f"\rProgress = {count}", end="")

    count = 0
    for key, val in new_output.items():
        if len(val["candidates"]) > 0:
            count += 1
    print("\nItems with at least 1 candidate = ", count)

    return new_output


def create_final_dataset(new_out, file_path):
    """
    Creates an error free final dataset in dict format
    :param new_out: the new json out file
    :param file_path: path to save the dict
    :return: None
    """
    data = {}
    count = 0
    for key, val in new_out.items():
        item = {
            "capital": 0,
            "symbol": ""
        }
        if len(val["candidates"]) > 0:
            c_name = val["c_name"].replace("_", "")
            for ele in val["candidates"]:
                name = ele[0].replace("_", "")
                ed = nltk.edit_distance(c_name.lower(), name.lower())
                similarity = 100 * (1 - ed / len(c_name))
                if similarity == 100.0 or key in ["L26942TG1979PLC002485", "U24230TG1998PLC029483"]:
                    if ele[1] == 0:
                        item["capital"] = "* Not Traded as on March 31, 2021"
                    else:
                        item["capital"] = ele[1]
                    item["symbol"] = ele[2]
                    break

        data[key] = item
        count += 1
        print(f"\rProgress = {count}", end="")

    file = open(file_path, "w+")
    json.dump(data, file, indent=4)
    file.close()


if __name__ == "__main__":
    output = parse_output("out.txt")
    create_final_dataset(output, "../../data/nseindia.com/final_data.json")

    # new_out = filter_output(output, 90)
    # file = open("new_out.json", "w+")
    # json.dump(new_out, file, indent=4)

    # file = open("new_out.json", "r")
    # out = json.load(file)
    # for key,val in out.items():
    #     if len(val["candidates"]) > 0:
    #         print(key, val)
    #         c_name = val["c_name"].replace("_","")
    #         new_candidates = []
    #         for ele in val["candidates"]:
    #             name = ele[0].replace("_","")
    #             ed = nltk.edit_distance(c_name.lower(), name.lower())
    #             similarity = 100 * (1 - ed / len(c_name))
    #             print(similarity)
    #             if similarity == 100.0:
    #                 break
    #         print()
    #         if similarity != 100:
    #             input("Press Enter")
    # file.close()
