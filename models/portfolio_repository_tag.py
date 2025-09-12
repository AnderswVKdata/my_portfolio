from odoo import fields, models
class PortfolioRepositoryTag(models.Model):
    _name="portfolio.repository.tag"
    _description="repository tag"
    name = fields.Char(required=True)
    
    portfolio_repository_ids = fields.Many2many(
        "portfolio.repository",
        "portfolio_repository_tag_rel",  # same relation table name
        "tag_id",          # this model's column (tag)
        "repository_id",   # related model's column (repository)
        string="Repositories"
    )
    #Ensures unique tags in database, comment out as i dont know if works
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Tag name must be unique!'),
    ]