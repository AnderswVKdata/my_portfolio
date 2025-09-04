from odoo import http
from odoo.http import request

class CustomWebsiteController(http.Controller):

    @http.route('/my-portfolio', type='http', auth="public", website=True)
    def homepage(self, **kw):
        repos = request.env['portfolio.repository'].sudo().search([('published', '=', True)])
        repo_list = []
        for i, repo in enumerate(repos, 1):
            repo_list.append({
                'name': repo.name,
                'html_url': repo.url,
                'description': repo.description,
                'index': i,
                'languages': [tag.name for tag in repo.portfolio_tag_ids],
            })
        print(f"REPOS SENT TO HOMEPAGE {repo_list}")

        return request.render("my_portfolio.homepage", {"repos": repo_list})

    @http.route('/publish-repos', type='http', auth="public", website=True)
    def publish_repo(self, **kw):
        return self._render_repos("my_portfolio.publish_repo")

    def _render_repos(self, template_name):
        github_user = "anderswvkdata"
        repos_data = request.env['portfolio.github.data.fetch'].sudo().fetch_repos(github_user)
        return request.render(template_name, {"repos": repos_data})
