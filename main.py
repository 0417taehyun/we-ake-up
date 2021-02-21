from config   import github_info, token
from worker   import 


def lambda_handler(event, context):
    user_name = github_info["user_name"]
    repo_name = github_info["repo_name"]

    url       = f"https://api.github.com/repos/{user_name}/{repo_name}"
    github_token     = token["GitHub"]
    headers   = {
        'Accept'       : 'application/vnd.github.v3+json',
        'Content-Type' : 'appliacation/json',
        'Authorization': f'Bearer {github_token}',
    }

