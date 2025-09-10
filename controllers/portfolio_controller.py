from odoo import http
from odoo.http import request


class CustomWebsiteController(http.Controller):

    @http.route('/my-portfolio', type='http', auth="public", website=True)
    def homepage(self, **kw):
        repos = request.env['portfolio.repository'].sudo().search([('published', '=', True)])
        repo_list = []
        all_tags = set()

        for i, repo in enumerate(repos, 1):
            tags = [tag.name for tag in repo.portfolio_tag_ids]
            repo_list.append({
                'name': repo.name,
                'html_url': repo.url,
                'description': repo.description,
                'index': i,
                'tags': tags,
            })
            all_tags.update(tags)

        # Convert set → list for QWeb
        unique_tags = list(all_tags)

        return request.render("my_portfolio.homepage_v2", {
            "repos": repo_list,
            "unique_tags": unique_tags,
        })

    @http.route('/publish-repos', type='http', auth="public", website=True)
    def publish_repo(self, **kw):
        return self._render_repos("my_portfolio.publish_repo")

    def _render_repos(self, template_name):
        github_user = "anderswvkdata"
        repos_data = request.env['portfolio.github.data.fetch'].sudo().fetch_repos(github_user)
        return request.render(template_name, {"repos": repos_data})

    @http.route('/aboutme', type='http', auth="public", website=True)
    def aboutme(self, **kw):
        info = request.env['portfolio.about.me.content'].sudo().get_record()
        partner_logo = request.env['portfolio.about.me.partner.logo'].sudo().get_record()
        experience_card = request.env['portfolio.about.me.experience.card'].sudo().get_record()
        return request.render("my_portfolio.aboutme_template", {
            'aboutme': info,
            'logos': partner_logo,
            'cards': experience_card,
        })