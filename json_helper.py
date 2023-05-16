import json
import os
import glob
import jsonlines

def json_to_jsonl(json_file_path):
    # Open the JSON file
    with open(json_file_path, 'r') as json_file:
        # Load the JSON data
        data = json.load(json_file)

    # Create a new file with the same name but with a .jsonl extension
    jsonl_file_path = json_file_path.replace('.json', '.jsonl')
    with open(jsonl_file_path, 'w') as jsonl_file:
        # Iterate through the data and write each item as a separate line in the JSONL file
        for item in data:
            json.dump(item,jsonl_file)
            jsonl_file.write('\n')

    delete_json_file()
    print(f"Successfully converted {json_file_path} to {jsonl_file_path}")


def delete_json_file():
    files = glob.glob('database/*.json')
    for f in files:
        os.remove(f)



# def update_jsonl():

#     with open('database/data.jsonl','a') as outfile:
#         for file in glob.glob('database/*.json'):
#             with open(file) as infile:
#                 json_data = json.load(infile)
#                 for obj in json_data:
#                     outfile.write(json.dumps(obj)+'\n')
#     delete_json_file()

def update_jsonl():
    with jsonlines.open('database/data.jsonl', mode='w') as outfile:
        for file in glob.glob('database/*.json'):
            with jsonlines.open(file) as infile:
                for obj in infile:
                    outfile.write(obj)
    delete_json_file()

json_to_jsonl("database/newdata1m.json")