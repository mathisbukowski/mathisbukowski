import requests
from datetime import datetime
import pytz
import os

GITHUB_API_URL = "https://api.github.com"
USERNAME = "mathisbukowski"
GITHUB_TOKEN = os.getenv('GH_TOKEN')
paris_tz = pytz.timezone('Europe/Paris')
now = datetime.now(paris_tz)

def fetch_repositories():
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return repos
    else:
        response.raise_for_status()

def fetch_commits(repo_name):
    url = f"{GITHUB_API_URL}/repos/{USERNAME}/{repo_name}/commits"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        return commits[:5]
    else:
        response.raise_for_status()

def update_readme(commits_by_repo):
    readme_path = "README.md"
    time = now.strftime("%H:%M:%S")

    try:
        with open(readme_path, "r") as readme_file:
            current_content = readme_file.read()
    except FileNotFoundError:
        current_content = ""

    new_commits_content = "\n\n## 🚦 Last commits on all repositories\n\n"
    for repo_name, commits in commits_by_repo.items():
        new_commits_content += f"\n### {repo_name}\n"
        for commit in commits:
            message = commit['commit']['message']
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            new_commits_content += f"\n🔸 - {message} from {author} at {date}\n"

    time_sentence = f"\n\n⏲ Updated at {time}"
    if "## 🚦 Last commits on all repositories" in current_content:
        updated_content = current_content.split("## 🚦 Last commits on all repositories")[0] + new_commits_content + time_sentence
    else:
        updated_content = current_content + new_commits_content + time_sentence

    with open(readme_path, "w") as readme_file:
        readme_file.write(updated_content)

if __name__ == "__main__":
    repositories = fetch_repositories()
    commits_by_repo = {}
    for repo in repositories:
        repo_name = repo['name']
        commits_by_repo[repo_name] = fetch_commits(repo_name)
    update_readme(commits_by_repo)
