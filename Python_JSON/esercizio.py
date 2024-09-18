import json

def JsonSerialize(data):
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

def JsonDeserialize(sFile):
    with open(sFile, "r") as read_file:
        return json.load(read_file)

def print_dictionary(dData):
    for keys, values in dData.items():
        print(keys,"\n",values)


sFilePath = "./Python_JSON/example_2.json"
data = JsonDeserialize(sFilePath)
print_dictionary(data)