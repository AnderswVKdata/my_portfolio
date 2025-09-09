from odoo import models, fields, api

class MyPartnerLogo(models.Model):
    _name="portfolio.about.me.partner.logo"
    _description="My Partner logos"

    image = fields.Image()
    name = fields.Text()

    about_me_id = fields.Many2one(
        "portfolio.about.me.content",
        string="About Me",
        ondelete="cascade"
    )

    @api.model
    def get_record(self):
        record = self.search([])
        return record