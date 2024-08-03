import requests
from datetime import datetime
import os
import pytz

GITHUB_API_URL = "https://api.github.com"
USERNAME = os.getenv('GH_USERNAME')
GITHUB_TOKEN = os.getenv('GH_TOKEN')

if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found.")

paris_tz = pytz.timezone('Europe/Paris')
now = datetime.now(paris_tz)

def fetch_repositories():
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    print(f"Fetching repositories: {response.status_code}")
    if response.status_code == 200:
        repos = response.json()
        return repos
    else:
        print(f"Failed to fetch repositories: {response.status_code} {response.text}")
        response.raise_for_status()

def fetch_commits(repo_name):
    url = f"{GITHUB_API_URL}/repos/{USERNAME}/{repo_name}/commits"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    print(f"Fetching commits for {repo_name}: {response.status_code}")
    if response.status_code == 200:
        commits = response.json()
        return commits
    else:
        print(f"Failed to fetch commits for {repo_name}: {response.status_code} {response.text}")
        response.raise_for_status()

def reformat_date(iso_date_str):
    date = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
    date = date.astimezone(paris_tz)
    return date.strftime('%Y-%m-%d %H:%M:%S %Z')

def update_readme(commits):
    readme_path = "README.md"
    time = now.strftime("%H:%M:%S")

    try:
        with open(readme_path, "r") as readme_file:
            current_content = readme_file.read()
    except FileNotFoundError:
        current_content = ""

    new_commits_content = "\n\n## 🚦 Last commits on all repositories\n\n"
    for commit in commits:
        repo_name = commit['repo_name']
        message = commit['commit']['message']
        date = reformat_date(commit['commit']['author']['date'])
        new_commits_content += f"\n🔸 - {message} at {date} in {repo_name}\n"

    time_sentence = f"\n\n⏲ Updated at {time}"
    if "## 🚦 Last commits on all repositories" in current_content:
        updated_content = current_content.split("## 🚦 Last commits on all repositories")[0] + new_commits_content + time_sentence
    else:
        updated_content = current_content + new_commits_content + time_sentence

    with open(readme_path, "w") as readme_file:
        readme_file.write(updated_content)

if __name__ == "__main__":
    try:
        repositories = fetch_repositories()
        all_commits = []
        for repo in repositories:
            repo_name = repo['name']
            print(f"Fetching commits for repository: {repo_name}")
            try:
                commits = fetch_commits(repo_name)
                for commit in commits:
                    commit['repo_name'] = repo_name
                all_commits.extend(commits)
            except requests.exceptions.HTTPError as e:
                print(f"Error fetching commits for {repo_name}: {e}")
        all_commits.sort(key=lambda x: x['commit']['author']['date'], reverse=True)
        recent_commits = all_commits[:10]
        update_readme(recent_commits)
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
