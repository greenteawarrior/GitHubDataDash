import sqlite3
import json
from pprint import pprint
import pandas as pd

with open('commits.json') as data_file:
    data = json.load(data_file)

sha = []
name = []
date = []
message = []
html_url = []
repo = []

for commit in data:
    sha.append(commit["sha"])
    name.append(commit["author"]["login"])
    date.append(commit["commit"]["committer"]["date"])
    message.append(commit["commit"]["message"])
    html_url.append(commit["html_url"])
    repo.append('/'.join(commit["html_url"].split('/')[3:5]))

df = pd.DataFrame({
        "sha": sha,
        "name": name,
        "date": date,
        "message": message,
        "html_url": html_url,
        "repo": repo
    })

conn = sqlite3.connect('commits_database')
df.to_sql('commits', conn, index=False, if_exists='append')