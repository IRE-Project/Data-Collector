'''@file
This file will generate the google search results
in text format to json format.
'''

### Necessary libraries to import
from os.path import exists
from os import listdir
import json


### Source directory containing txt files (output files of google search)
source = "Google Search/"

### Define the parameters to run
top_url_c = 0
data = {}
index = 1

if exists(source):
    for file_ in listdir(source):
        print("Processing: ", file_)

        ### Reading the output file contents
        lines = []
        with open(source+file_, "r") as fp:
            lines = fp.readlines()

        ### For each line processing the format
        for line in lines:
            try:
                ### Processing each line
                line = line.replace("\n","").replace("\r","")
                line = eval(line)
                if len(line['top_urls'])>0:
                    top_url_c += 1

                ### Adding to the dictionary
                data[str(index)] = line
                index += 1

            except Exception as e:
                print(e)

    ### Stats of output
    print("Length: ",len(data))
    print("Top Url Count: ",str(top_url_c))

    ### Writing results to the json file.
    with open("Google_search.json", "w") as fp:
        json.dump(data, fp)

else:
    print(source, " path not found")