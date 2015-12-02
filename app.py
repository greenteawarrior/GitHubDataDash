from crud import DBWrapper

schema = ["link", "person", "time", "body", "repo_owner", "repo_name", "pr_number", "pr_updated_at"]
dbw = DBWrapper('pr_comments_db.sqlite')

def construct_repo_url(repo_owner, repo_name):
	return "https://www.github.com/{repo_owner}/{repo_name}"\
		.format(repo_owner=repo_owner, repo_name=repo_name)

def construct_pull_request_url_v1(repo_owner, repo_name, number):
	return "https://www.github.com/{repo_owner}/{repo_name}/pull/{n}"\
		.format(repo_owner=repo_owner, repo_name=repo_name, n=number)

def construct_pull_request_url_v2(comment_url):
	return comment_url.split('#')[0]

def get_comments_wrapup_for_repo(repo_owner, repo_name):
	comments_res = dbw.get_comments_for_repo(repo_owner, repo_name)
	pull_requests = {}
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
		pull_requests[tmp["pr_number"]] = construct_pull_request_url_v2(tmp['link'])
	# add the pull requests at the end
	for number, url in pull_requests.iteritems():
		wrapup["pull_requests"].append({
			"number": number,
			"url": url
		})
	return wrapup

if __name__ == '__main__':
	wrapup = get_comments_wrapup_for_repo('mila-udem','blocks')
