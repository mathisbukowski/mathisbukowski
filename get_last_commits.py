import requests
import os

GITHUB_API_URL = "https://api.github.com"
REPO = "mathisbukowski/Railess"

def fetch_commits():
    url = f"{GITHUB_API_URL}/repos/{REPO}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()
        return commits[:5]
    else:
        return []

def update_readme(commits):
    readme_content = "# Last commits\n\n"
    for commit in commits:
        message = commit['commit']['message']
        author = commit['commit']['author']['name']
        date = commit['commit']['author']['date']
        readme_content += f"- {message} from {author} at {date}\n"

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

if __name__ == "__main__":
    commits = fetch_commits()
    update_readme(commits)