import requests

#var to hold url
url = "http://localhost:7474/db/data/transaction/commit"
import json

#format the headers
headers = {
    'accept': "application/json; charset=UTF-8",
    'content-type': "application/json"
    }

#init payload format
batch = []
payload = {
            "statements": [{
                "statement": ""
            }]
        }

#open the init.txt file and roll through each line.
with open('init.txt', 'r') as f:
    for line in f:
        #construct the dict/list with the data from the file.  Creates one big line

        batch.append({"statement": line})


payload["statements"] = batch
print json.dumps(payload)

f.close()
#post request to node4j.  Input the url, payload and the formated headers
response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
print response.text






