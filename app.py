# flask imports
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import jsonify
from flask import render_template

# std imports
from itertools import chain

# local imports
from crud import DBWrapper

SCHEMA = ["link", "person", "time", "body", "repo_owner", "repo_name", "pr_number", "pr_updated_at"]

def construct_repo_url(repo_owner, repo_name):
    return "https://www.github.com/{repo_owner}/{repo_name}"\
        .format(repo_owner=repo_owner, repo_name=repo_name)

def construct_pull_request_url_v1(repo_owner, repo_name, number):
    return "https://www.github.com/{repo_owner}/{repo_name}/pull/{n}"\
        .format(repo_owner=repo_owner, repo_name=repo_name, n=number)

def construct_pull_request_url_v2(comment_url):
    return comment_url.split('#')[0]

def get_comments_wrapup_for_repo(dbw, repo_owner, repo_name):

    comments_res = dbw.get_comments_for_repo(repo_owner, repo_name)
    # try except to handle empty query result
    # source: http://stackoverflow.com/questions/11630207/how-can-i-check-if-sqlite-cursor-result-from-a-select-statement-is-empty
    try:
        first_row = next(comments_res)
        pull_requests = {}
        for i, result in enumerate(chain((first_row,), comments_res)):
            tmp = dict(zip(SCHEMA, result))
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

    except StopIteration as e:
        return {"error": "Query result returned empty"} # 0 results

@app.route('/repo_roster/<repo_owner>/<repo_name>')
def repo_roster(repo_owner, repo_name):
    dbw = DBWrapper('pr_comments_db.sqlite')
    wrapup = get_comments_wrapup_for_repo(dbw, repo_owner, repo_name)
    return jsonify(**wrapup)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')
    # error = None
    # if request.method == 'POST':
    #     if valid_login(request.form['username'],
    #                    request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #         error = 'Invalid username/password'
    # # the code below is executed if the request method
    # # was GET or the credentials were invalid
    # return render_template('login.html', error=error)

if __name__ == '__main__':
    # # wrapup = get_comments_wrapup_for_repo('mila-udem','blocks')
    app.run(debug=True)