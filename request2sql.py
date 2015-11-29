from __future__ import unicode_literals
from crud import DBWrapper
import requests
import utils
import json

# Whether to make API calls, or read JSON from backup.  Good for solving Rate Limiting
ONLINE = False

def extract_features_from_comment(comment):
    return {
        "person": comment["user"]["login"],
        "time" : comment["updated_at"],
        "body" : comment["body"],
        "link" : comment["html_url"]
    }

# instantiate db and table
dbw = DBWrapper("pr_comments_db.sqlite")
# dbw.create_comments_table()

if ONLINE:
    pr_list_api_url = "https://api.github.com/repos/mila-udem/blocks/pulls"
    pr_list = requests.get(pr_list_api_url).json()
    with open('pr_list.json', 'w') as fp:
        json.dump(pr_list, fp)
else:
    with open('pr_list.json', 'r') as fp:
        pr_list = json.load(fp)

for i, pr in enumerate(pr_list):
    repo_owner, repo_name = pr["url"].split('/')[4:6]
    pr_schema = {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "pr_number": pr["number"],
        "pr_updated_at": pr["updated_at"] 
    }

    if ONLINE:
        review_comments = requests.get(pr["_links"]["review_comments"]["href"]).json()
        issue_comments = requests.get(pr["_links"]["issue"]["href"] + "/comments").json()
        with open('review_comments%d.json' % i, 'w') as fp:
            json.dump(review_comments, fp)
        with open('issue_comments%d.json' % i, 'w') as fp:
            json.dump(issue_comments, fp)
    else:
        with open('review_comments%d.json' % i, 'r') as fp:
            review_comments = json.load(fp)
        with open('issue_comments%d.json' % i, 'r') as fp:
            issue_comments = json.load(fp)


    for comment in review_comments:
        comment_schema = extract_features_from_comment(comment)
        comment_schema.update(pr_schema)
        comment_schema = {key: utils.format_quotes(value) for (key, value) in comment_schema.iteritems()}
        try:
            dbw.upsert_comment(**comment_schema)
        except Exception, e:
            print e
            import ipdb; ipdb.set_trace();

    for comment in issue_comments:
        comment_schema = extract_features_from_comment(comment)
        comment_schema.update(pr_schema)
        comment_schema = {key: utils.format_quotes(value) for (key, value) in comment_schema.iteritems()}
        try:
            dbw.upsert_comment(**comment_schema)
        except Exception, e:
            print e
            import ipdb; ipdb.set_trace();
