import requests
from datetime import datetime

GITHUB_API_URL = "https://api.github.com"
REPO = "mathisbukowski/Railess"
now = datetime.now()

def fetch_commits():
    url = f"{GITHUB_API_URL}/repos/{REPO}/commits"
    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()
        return commits[:5]
    else:
        return []

def update_readme(commits):
    readme_path = "README.md"

    time = now.strftime("%H:%M:%S")

    try:
        with open(readme_path, "r") as readme_file:
            current_content = readme_file.read()
    except FileNotFoundError:
        current_content = ""

    new_commits_content = "\n\n## 🚦 Last commits on Railess\n\n"
    for commit in commits:
        message = commit['commit']['message']
        author = commit['commit']['author']['name']
        date = commit['commit']['author']['date']
        new_commits_content += f"\n\n🔸 - {message} from {author} at {date}\n"

    time_sentence = f"\n\n ⏱ Updated at {time}"
    if "## 🚦 Last commits on Railess" in current_content:
        updated_content = current_content.split("## 🚦 Last commits on Railess")[0] + new_commits_content + time_sentence
    else:
        updated_content = current_content + new_commits_content + time_sentence

    with open(readme_path, "w") as readme_file:
        readme_file.write(updated_content)

if __name__ == "__main__":
    commits = fetch_commits()
    update_readme(commits)
