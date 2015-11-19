import json
from pprint import pprint

with open('commits.json') as data_file:
    data = json.load(data_file)

pprint(data[0])

# print
# pprint(data[0].keys())

# pprint(data[0]['committer'])