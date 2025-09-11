from odoo import http
from odoo.http import request


class CustomWebsiteController(http.Controller):
    
    @http.route('/my-portfolio', type='http', auth="public", website=True)
    def homepage(self, **kw):
        repo_list, unique_tags = self._get_repos_and_tags()
        return request.render("my_portfolio.homepage_v2", {
            "repos": repo_list,
            "unique_tags": unique_tags,
        })

    # AJAX filter route (returns only the carousel inner template)
    @http.route('/portfolio/filter', type='json', auth="public", website=True)
    def filter_repos(self, tags=None, **kw):
        repo_list, _ = self._get_repos_and_tags()

        # Apply filter if tags selected
        if tags:
            filtered = []
            for repo in repo_list:
                if set(tags).issubset(set(repo.get("tags", []))):
                    filtered.append(repo)
            repo_list = filtered

        return request.env['ir.ui.view']._render_template(
            "my_portfolio.carousel_inner",
            {"repos": repo_list}
        )
  
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
    
    #Fetches published repos
    def _get_repos_and_tags(self):
        repos = request.env['portfolio.repository'].sudo().search([('published', '=', True)])
        repo_list = []
        all_tags = set()

        for i, repo in enumerate(repos, 1):
            tag_names = [tag.name for tag in repo.portfolio_tag_ids]
            repo_list.append({
                'name': repo.name,
                'html_url': repo.url,
                'description': repo.description,
                'index': i,
                'tags': tag_names,
            })
            all_tags.update(tag_names)

        return repo_list, list(all_tags)
    

