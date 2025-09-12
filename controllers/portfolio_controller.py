from odoo import http
from odoo.http import request, Response
import logging
_logger = logging.getLogger(__name__)


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
    
    @http.route('/contactme', type='http', auth='public', website=True)
    def contact_me_page(self, **kw):
        # simple render that includes a marker so we can confirm source
        return request.render('my_portfolio.contact_me_page')

    # Debug endpoint: logs post, creates record, and returns plain text (no redirect)
    @http.route('/contactme/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def contact_me_submit(self, **post):
        _logger.info("DEBUG: /contact-me/submit HIT, post=%s", post)
        try:
            vals = {
                'name': post.get('name') or False,
                'phone': post.get('phone') or False,
                'email_from': post.get('email_from') or False,
                'company': post.get('company') or False,
                'subject': post.get('subject') or False,
                'question': post.get('question') or False,
            }
            rec = request.env['portfolio.contact.me'].sudo().create(vals)
            _logger.info("DEBUG: created portfolio.contact.me id=%s vals=%s", rec.id, vals)
            # return plain text showing created id for easy testing
            return Response("OK: created id=%s" % rec.id, status=200, mimetype='text/plain')
        except Exception as e:
            _logger.exception("DEBUG: create failed: %s", e)
            return Response("ERROR: %s" % e, status=500, mimetype='text/plain')

    
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
    

