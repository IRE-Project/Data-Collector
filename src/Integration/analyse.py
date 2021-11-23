"""@file
This file is responsible for analysis of the final dataset.
"""
import json


def create_col_list(data):
    columns = set()
    for key,val in data.items():
        try:
            for col in val.keys():
                columns.add(col)
        except Exception as e:
            print(key)
    return columns


def calc_sparsity(data, columns):

    for cin, val in data.items():
        columns["CIN/LLPIN"] += 1
        for col, col_val in val.items():
            if col == "NSE":
                if col_val["symbol"] != "":
                    columns[col] += 1
            elif col_val != "" and col_val != [] and col_val != {}:
                columns[col] += 1
    te = sum(columns.values())
    for key, val in columns.items():
        columns[key] = val * 100 / len(data)
    return columns, te


if __name__ == "__main__":
    file = open("../../data/integrated.json")
    data = json.load(file)
    file.close()

    columns = create_col_list(data)
    columns.add("CIN/LLPIN")
    col_dict = {}
    for ele in columns:
        col_dict[ele] = 0
    sparsity, te = calc_sparsity(data, col_dict)


    for col, sp in sparsity.items():
        print(col, ": ", sp)
    print("Average: ", sum(sparsity.values())/len(sparsity))
    print("Total Entries: ", te)
    print("Average Sparsity: ", te * 100 / (len(sparsity) * len(data)))
    print(f"Column count: {len(columns)}")