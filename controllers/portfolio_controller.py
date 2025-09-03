from odoo import http
from odoo.http import request

class CustomWebsiteController(http.Controller):

    @http.route('/', type='http', auth="public", website=True)
    def homepage(self, **kw):
        return self._render_repos("my_portfolio.homepage")

    @http.route('/publish-repo', type='http', auth="public", website=True)
    def publish_repo(self, **kw):
        return self._render_repos("my_portfolio.publish_repo")

    def _render_repos(self, template_name):
        github_user = "anderswvkdata"
        repos_data = request.env['github.repo'].sudo().fetch_repos(github_user)
        return request.render(template_name, {"repos": repos_data})
