from odoo import models, api

class ContactEmailService(models.AbstractModel):
    _name = 'contact.email.service'
    _description = 'Service for sending emails'

    @api.model
    def send_contact_form_emails(self, name, email_from, phone, company, subject, question):
        email_to = 'andersw@vkdata.dk'  

        # Email to admin
        body_html_admin = f"""
        <div style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; border-radius: 8px;">
            <h2 style="color: #2f80ed;">New Contact Form Submission</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email_from}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Company:</strong> {company}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Question:</strong><br>{question}</p>
        </div>
        """

        self.env['mail.mail'].sudo().create({
            'subject': f'Contact Form: {subject}',
            'body_html': body_html_admin,
            'email_from': email_from,
            'email_to': email_to,
        }).send()

        # Auto-reply to user
        body_html_auto_reply = f"""
        <div style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; border-radius: 8px;">
            <h2 style="color: #2f80ed;">Thank You for Contacting Me</h2>
            <p>Hi {name},</p>
            <p>Thank you for reaching out! I have received your message and will get back to you shortly.</p>
            <p>Best regards,<br>Your Name / Company</p>
        </div>
        """

        self.env['mail.mail'].sudo().create({
            'subject': 'Thank you for contacting me',
            'body_html': body_html_auto_reply,
            'email_from': email_to,  
            'email_to': email_from,  
        }).send()

