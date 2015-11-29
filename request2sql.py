from crud import DBWrapper
import requests

def extract_features_from_comment(comment):
    return {
	    "person": comment["user"]["login"],
	    "time" : comment["updated_at"],
	    "body" : comment["body"],
	    "link" : comment["html_url"]    
    }

# instantiate db and table
dbw = DBWrapper("pr_comments_db.sqlite")
dbw.create_comments_table()

pr_list_api_url = "https://api.github.com/repos/mila-udem/blocks/pulls"
pr_list = requests.get(pr_list_api_url).json()
for pr in pr_list:
    repo_owner, repo_name = pr["url"].split('/')[4:6]
    pr_number = pr["number"]
    pr_updated_at = pr["updated_at"]

    review_comments = requests.get(pr["_links"]["review_comments"]["href"]).json()
    issue_comments = requests.get(pr["_links"]["issue"]["href"] + "/comments").json()

    for comment in review_comments:
    	comment_schema = extract_features_from_comment(comment)
    	comment_schema["repo_owner"] = repo_owner
    	comment_schema["repo_name"] = repo_name
    	comment_schema["pr_number"] = pr_number
    	comment_schema["pr_updated_at"] = pr_updated_at
    	dbw.upsert_comment(**comment_schema)

    for comment in issue_comments:
    	comment_schema = extract_features_from_comment(comment)
    	comment_schema["repo_owner"] = repo_owner
    	comment_schema["repo_name"] = repo_name
    	comment_schema["pr_number"] = pr_number
    	comment_schema["pr_updated_at"] = pr_updated_at
    	dbw.upsert_comment(**comment_schema)
