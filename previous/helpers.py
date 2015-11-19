
# Some common variables
# repo - string of name of repository
# user - string of user's GitHub account
# since_time - datetime string of how far back to investigate commits
#              should match the datetime format that the GitHub API uses

# TODO: Discussion points
# store a dictionary with mappings of repo name to URL for the API call
# store a dictionary of user strings and repos that the user commits to
# commits since time X? or commits between t and t-interval?
# commits that have happened that hour
# commits that have happened that day
# visualization of commit trends for the a specific start day and end day

def repo_commits_since (repo, user, since_time):
    # returns the number of commits a repo has had since time X

    return num_repo_commits_since

def user_commits_since (repo, user, since_time):
    # returns the number of commits a user made for a given repo sicne time X

    return num_user_commits_since