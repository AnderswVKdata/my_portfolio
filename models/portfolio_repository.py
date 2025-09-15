from datetime import date
from odoo import fields, models, api

class PortfolioRepository(models.Model):
    _name="portfolio.repository"
    _description="Portfolio Repository"

    name = fields.Char()
    url = fields.Char()
    description = fields.Text()
    published = fields.Boolean(default=False)
    end_date = fields.Date()

    portfolio_tag_ids = fields.Many2many(
        "portfolio.repository.tag",
        "portfolio_repository_tag_rel",  # relation table name
        "repository_id",  # this model's column
        "tag_id",         # related model's column
        string="Repository Tags"
    )
    

    
    #ensures that end_date is in the future on creation
    @api.model_create_multi
    def create(self, vals):
        """Apply same check on create"""
        record = super().create(vals)
        if record.end_date and record.end_date < date.today():
            record.published = False
        return record
    
    #unpublish records where end date has passed
    def unpublish_expired_repo(self):
        today = date.today()
        expired = self.search([('published', '=', True), ('end_date', '<', today)])
        expired.write({'published': False})