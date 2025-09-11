from odoo import fields,models

class CardTag(models.Model):
    _name="portfolio.about.me.card.tag"
    _description="Code Language Tags For Cards"

    name = fields.Char(string="Name", required=True)

    #_sql_constraints = [
    #    ('unique_tag_name', 'unique(name)', 'Tag name must be unique!'),
    #]