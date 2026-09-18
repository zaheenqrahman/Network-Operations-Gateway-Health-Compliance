import requests
import json

response = requests.get(
    'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
# print response gives you the id number 200, print json gives you all the items, ids
# ' items ' gives you all the items lsit

# queries and searches through all titles with for loop
for data in  response.json()['items']:
    if data['answer_count'] == 0:
        print(data['title'])
        print(data['link']) # gives you links of data with title
    else:
        print("skipped")
    print()

# this calls information/data in an API