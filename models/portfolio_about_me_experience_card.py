from odoo import fields, models, api

class ExperienceCard(models.Model):
    _name="portfolio.about.me.experience.card"
    _description="Experience cards"

    title = fields.Char(string="Title")          
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")

    card_tag_ids = fields.Many2many(
        "portfolio.about.me.card.tag",
        "portfolio_card_tag_rel",  # shorter relation table name
        "card_id",                 
        "tag_id",                  
        string="Language Card Tags"
    )

    @api.model
    def get_record(self):
        record = self.search([])
        return record


    

