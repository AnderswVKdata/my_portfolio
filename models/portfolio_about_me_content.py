from odoo import models, fields, api, exceptions

class AboutMeContent(models.Model):
    _name="portfolio.about.me.content"
    _description="editable about me content"

    name = fields.Text(string="Name")
    title = fields.Text(string="Title")
    description = fields.Text(string="Description")
    address = fields.Text(string="Address")
    image = fields.Image(string="Profile Picture")

    partner_logo_ids = fields.One2many(
        "portfolio.about.me.partner.logo",
        "about_me_id",
        string="Partner Logos"
    )

    @api.model
    def get_record(self):
        """Always return the single record (create it if missing)."""
        record = self.search([], limit=1)
        if not record:
            record = self.create({})
        return record
    
    #Singleton create record, if one exist update instead of creating multiple
    @api.model_create_multi
    def create(self, vals_list):
        if len(vals_list) > 1:
            raise exceptions.UserError(
                "Batch creation not supported. Only one About Me record is allowed."
            )

        vals = vals_list[0]
        existing = self.search([], limit=1)
        if existing:           
            keys_to_remove = [
                key for key, value in vals.items()
                if not value and value != 0
            ]
            for key in keys_to_remove:
                vals.pop(key)

            existing.write(vals)
            return existing
        else:
            return super().create(vals_list)