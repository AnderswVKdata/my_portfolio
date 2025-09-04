from odoo import models, fields
class GitHubRepoWizard(models.TransientModel):
    _name = 'portfolio.github.repo.wizard'
    _description = 'GitHub Repo Wizard'

    github_username = fields.Char(string="GitHub Username")

    def action_fetch_repos(self):
        github_service = self.env['portfolio.github.data.fetch']
        repo_data = github_service.fetch_repos(self.github_username)

        for repo in repo_data:
            tag_ids = []
            for lang in repo['languages']:
                tag = self.env['portfolio.repository.tag'].sudo().search([('name', '=', lang)], limit=1)
                if not tag:
                    tag = self.env['portfolio.repository.tag'].sudo().create({'name': lang})
                tag_ids.append(tag.id)

            existing_repo = self.env['portfolio.repository'].sudo().search([('url', '=', repo['html_url'])], limit=1)
            if existing_repo:
                existing_repo.write({
                    'name': repo['name'],
                    'description': repo['description'],
                    'portfolio_tag_ids': [(6, 0, tag_ids)],
                    'published': False,
                })
            else:
                self.env['portfolio.repository'].sudo().create({
                    'name': repo['name'],
                    'url': repo['html_url'],
                    'description': repo['description'],
                    'portfolio_tag_ids': [(6, 0, tag_ids)],
                    'published': False,
                })

        return {'type': 'ir.actions.act_window_close'}

    def action_clear_repos(self):
        # Delete all repositories
        self.env['portfolio.repository'].sudo().search([]).unlink()

        # Also clear tags not linked to any repositories
        unused_tags = self.env['portfolio.repository.tag'].sudo().search([
            ('portfolio_repository_ids', '=', False)
        ])
        unused_tags.unlink()

