import json


def dictlinks_to_list():
    file = open("../../data/zaubacorp.com/links.json", "r")
    links = json.load(file)
    file.close()

    data = []
    for key, val in links.items():
        row = [key, val["Company"], val["RoC"], val["Status"], val["link"]]
        data.append(row)

    print(len(data))

    file = open("../../data/zaubacorp.com/linkslist.json", "w+")
    json.dump({"data": data}, file, indent=4)
    file.close()


dictlinks_to_list()