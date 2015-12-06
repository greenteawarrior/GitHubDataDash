from __future__ import unicode_literals
from crud import DBWrapper
import requests
import json
import os

from config import OAUTH_TOKEN

# Whether to make API calls, or read JSON from backup.  Good for solving Rate Limiting
ONLINE = True
DUMP = False

def extract_features_from_comment(comment):
    """ extracts features from comment for the sql schema

    Parameters
    ----------
    comment: dict

    Returns
    -------
    comment_schema: dict
    """
    return {
        "person": comment["user"]["login"],
        "time" : comment["updated_at"],
        "body" : comment["body"],
        "link" : comment["html_url"],
        "avatar_url": comment['user']['avatar_url']
    }

def extract_features_from_pr(pr):
    """ extracts features from pr for the sql schema

    Parameters
    ----------
    pr: dict

    Returns
    -------
    pr_schema: dict
    """
    repo_owner, repo_name = pr["url"].split('/')[4:6]
    return {
        "repo_owner": repo_owner,
        "repo_name": repo_name,
        "pr_number": pr["number"],
        "pr_updated_at": pr["updated_at"]
    }

def request_pr_list(repo_owner, repo_name):
    """ make a github api request for the pr list

    Parameters
    ----------
    owner: str
    repo: str

    Returns
    -------
    pr_list: list of json objects
    """
    pr_list_api_url = "https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?access_token={OAUTH_TOKEN}"\
        .format(repo_owner=repo_owner, repo_name=repo_name, OAUTH_TOKEN=OAUTH_TOKEN)
    print pr_list_api_url
    pr_list = requests.get(pr_list_api_url).json()
    return pr_list

def request_all_comments(repo_owner, repo_name):
    # instantiate db and table
    db_name = "pr_comments_db.sqlite"
    # FIX: long term solution to creating tables if they don't exist
    if not os.path.exists(db_name):
        dbw = DBWrapper(db_name)
        print("Creating DB: {}".format(db_name))
        dbw.create_comments_table()
    else:
        dbw = DBWrapper(db_name)

    if ONLINE:
        pr_list = request_pr_list(repo_owner, repo_name)
        if DUMP:
            with open('pr_list.json', 'w') as fp:
                json.dump(pr_list, fp)
    else:
        with open('pr_list.json', 'r') as fp:
            pr_list = json.load(fp)

    for i, pr in enumerate(pr_list):
        pr_schema = extract_features_from_pr(pr)

        if ONLINE:
            review_comments = requests.get(pr["_links"]["review_comments"]["href"]).json()
            issue_comments = requests.get(pr["_links"]["issue"]["href"] + "/comments").json()
            if DUMP:
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
            dbw.upsert_comment(**comment_schema)

        for comment in issue_comments:
            comment_schema = extract_features_from_comment(comment)
            comment_schema.update(pr_schema)
            dbw.upsert_comment(**comment_schema)

if __name__ == '__main__':
    request_all_comments("OlinMobileProto", "Lab1")
    request_all_comments("OlinMobileProto", "Lab2")
    request_all_comments("OlinMobileProto", "Lab3")