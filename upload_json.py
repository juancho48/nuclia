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


def read_json(path):
    with open(path) as jsonfile:
        # create a reader for a json type file and read the file
        data = json.load(jsonfile)
        for row in data["links"]:
            upload(row)

if __name__ == "__main__":
    read_json('wikis.json')