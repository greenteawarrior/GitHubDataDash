from crud import DBWrapper

schema = ["link", "person", "time", "body", "repo_owner", "repo_name", "pr_number", "pr_updated_at"]
dbw = DBWrapper('pr_comments_db.sqlite')

def construct_repo_url(repo_owner, repo_name):
	return "https://www.github.com/{repo_owner}/{repo_name}"\
		.format(repo_owner=repo_owner, repo_name=repo_name)

def get_comments_wrapup_for_repo(repo_owner, repo_name):
	comments_res = dbw.get_comments_for_repo(repo_owner, repo_name)
	for i, result in enumerate(comments_res):
		tmp = dict(zip(schema, result))
		if i == 0:
			# create wrapup before adding comments or pull requests
			wrapup = {
				"repo_owner": tmp["repo_owner"],
				"repo_name": tmp["repo_name"],
				"repo_url": construct_repo_url(tmp["repo_owner"], tmp["repo_name"]),
				"comments": [],
				"pull_requests": []
			}
		comment = {
			"person": tmp["person"],
			"body": tmp["body"],
			"url": tmp["link"],
			"time": tmp["time"]
		}
		wrapup["comments"].append(comment)
		# add PR info
	return wrapup

if __name__ == '__main__':
	wrapup = get_comments_wrapup_for_repo('mila-udem','blocks')