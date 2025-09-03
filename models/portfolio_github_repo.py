from odoo import models
import requests
import os

class GitHubRepo(models.AbstractModel):
    _name = 'github.repo'
    _description = 'GitHub Repo Service'

    def fetch_repos(self, github_user):
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

            for i, repo in enumerate(repos, 1):
                readme_url = f"https://raw.githubusercontent.com/{github_user}/{repo['name']}/main/README.md"
                readme_response = requests.get(readme_url)

                repos_data.append({
                    "name": repo["name"],
                    "html_url": repo["html_url"],
                    "description": readme_response.text if readme_response.status_code == 200 else "No description available.",
                    "index": i,
                })

        except Exception as e:
            repos_data.append({
                "name": "Error",
                "html_url": "#",
                "description": str(e),
                "index": 1
            })

        return repos_data
