from config   import github_info, token
from worker   import Worker


def lambda_handler():
    user_name = github_info["user_name"]
    repo_name = github_info["repo_name"]

    url       = f"https://api.github.com/repos/{user_name}/{repo_name}"
    github_token     = token["GitHub"]
    headers   = {
        'Accept'       : 'application/vnd.github.v3+json',
        'Content-Type' : 'appliacation/json',
        'Authorization': f'Bearer {github_token}',
    }
    
    worker = Worker(url, headers)

    worker.create_issue()
    worker.close_issue()

