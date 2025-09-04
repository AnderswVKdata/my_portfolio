from odoo import fields, models

class PortfolioRepository(models.Model):
    _name="portfolio.repository"
    _description="Portfolio Repository"

    name = fields.Char()
    url = fields.Char()
    description = fields.Text()
    published = fields.Boolean(default=False)

    portfolio_tag_ids = fields.Many2many(
        "portfolio.repository.tag",
        "portfolio_repository_tag_rel",  # relation table name
        "repository_id",  # this model's column
        "tag_id",         # related model's column
        string="Repository Tags"
    )
    
    
