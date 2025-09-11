from odoo import fields,models

class CardTag(models.Model):
    _name="portfolio.about.me.card.tag"
    _description="Code Language Tags For Cards"

    name = fields.Char(string="Name", required=True)

    # Ensures unique card tags in database, comment out as i dont know if works
    #_sql_constraints = [
    #    ('unique_tag_name', 'unique(name)', 'Tag name must be unique!'),
    #]