from odoo import models, fields

class ContactMe(models.Model):
    _name="portfolio.contact.me"
    _description="Messages sent to me"

    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone Number")
    email_from = fields.Char(string="E-mail")
    company = fields.Char(string="Company")
    subject = fields.Char(string="Subject")
    question = fields.Text(string="Your Question")