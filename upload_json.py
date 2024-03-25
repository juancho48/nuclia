import sys
# print(sys.executable)
import json
from nuclia import sdk

KNOWLEDGE_BOX = "https://aws-us-east-2-1.nuclia.cloud/api/v1/kb/f08a00d7-4348-4730-9b77-7fa0bc21851c"
API_KEY = "API_TOKEN"

sdk.NucliaAuth().kb(url=KNOWLEDGE_BOX, token=API_KEY)

def upload(row):
    upload = sdk.NucliaUpload()
    upload.link(uri=row['url'])
    print(f'Uploading {row["url"]}')

def links_in_kb():
    kb = sdk.NucliaKB()
    resources = kb.list(interactive=False)
    just_titles =  [x.title for x in resources.resources] # return a dictionary of resources
    return just_titles

def title_in_dict(myList, title):
    return any(s for s in myList if title in s)

def read_json(path):
    existingList = links_in_kb()
    with open(path) as jsonfile:
        # create a reader for a json type file and read the file
        data = json.load(jsonfile)
        for row in data["links"]:
            # Extract the last part of the URL and replace underscores with spaces
            extracted_name = row['url'].split('/')[-1].replace('_', ' ')
            # Check if it already exists in the KB, then don't upload
            if title_in_dict(existingList, extracted_name):
                print(f'Do Not Upload {extracted_name}')
            else:
                print(f'Uploading {extracted_name}')
                upload(row)

if __name__ == "__main__":
    read_json('wikis.json')