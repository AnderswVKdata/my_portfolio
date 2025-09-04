from odoo import models
import requests
import os


class GitHubRepo(models.AbstractModel):
    _name = 'portfolio.github.data.fetch'
    _description = 'GitHub Repo Fetch Service'

    def fetch_repos(self, github_user):
        print("GitHub repo has been called")
        token = os.getenv("GITHUB_TOKEN")
        repo_api_url = f"https://api.github.com/users/{github_user}/repos"
        repos_data = []

        headers = {}
        if token:
            headers['Authorization'] = f'token {token}'

        try:
            response = requests.get(repo_api_url, headers=headers)
            response.raise_for_status()
            repos = response.json()

            for repo in repos:
                readme_url = f"https://raw.githubusercontent.com/{github_user}/{repo['name']}/main/README.md"
                readme_response = requests.get(readme_url)

                languages_url = f"https://api.github.com/repos/{github_user}/{repo['name']}/languages"
                lang_response = requests.get(languages_url, headers=headers)
                lang_response.raise_for_status()
                languages_data = lang_response.json()

                repos_data.append({
                    "name": repo["name"],
                    "html_url": repo["html_url"],
                    "description": readme_response.text if readme_response.status_code == 200 else "No description available.",
                    "languages": list(languages_data.keys()),
                })

        except Exception as e:
            repos_data.append({
                "name": "Error",
                "html_url": "#",
                "description": str(e),
                "languages": []
            })

        return repos_data