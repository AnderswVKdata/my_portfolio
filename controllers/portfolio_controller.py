from odoo import http
from odoo.http import request, Response

class CustomWebsiteController(http.Controller):
    
    @http.route('/my-portfolio', type='http', auth="public", website=True)
    def homepage(self, **kw):
        repo_list, unique_tags = self._get_repos_and_tags()
        return request.render("my_portfolio.homepage_v2", {
            "repos": repo_list,
            "unique_tags": unique_tags,
        })

    # AJAX filter route (returns only the carousel inner template)
    #js sends list of tags to route as json
    @http.route('/portfolio/filter', type='json', auth="public", website=True)
    #tags are from the json payload
    def filter_repos(self, tags=None, **kw):
        repo_list, _ = self._get_repos_and_tags()

        # Apply filter if tags selected
        if tags:
            filtered = []
            for repo in repo_list:
                if set(tags).issubset(set(repo.get("tags", []))):
                    filtered.append(repo)
            repo_list = filtered

        return request.env['ir.ui.view']._render_template(
            "my_portfolio.carousel_inner",
            {"repos": repo_list}
        )
  
    @http.route('/aboutme', type='http', auth="public", website=True)
    def aboutme(self, **kw):
        info = request.env['portfolio.about.me.content'].sudo().get_record()
        partner_logo = request.env['portfolio.about.me.partner.logo'].sudo().get_record()
        experience_card = request.env['portfolio.about.me.experience.card'].sudo().get_record()
        return request.render("my_portfolio.aboutme_template", {
            'aboutme': info,
            'logos': partner_logo,
            'cards': experience_card,
        })
    
    @http.route('/contactme', type='http', auth='public', website=True)
    def contact_me_page(self, **kw):
        return request.render('my_portfolio.contact_me_page')


    @http.route('/contactme/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def contact_me_submit(self, **post):
        # Extract variables from post
        name = post.get('name')
        phone = post.get('phone')
        email_from = post.get('email_from')
        company = post.get('company')
        subject = post.get('subject')
        question = post.get('question')

        # Prepare values for model
        vals = {
            'name': name,
            'phone': phone,
            'email_from': email_from,
            'company': company,
            'subject': subject,
            'question': question,
        }

        email_to = 'andersw@vkdata.dk'  
        # Email body
        body_html = f"""
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
        # Send email
        mail_values = {
            'subject': f'Contact Form: {subject}',
            'body_html': body_html,
            'email_from': email_from,
            'email_to': email_to,
        }
        request.env['mail.mail'].sudo().create(mail_values).send()

           # Email 2: Auto-reply to the user
        body_html_auto_reply = f"""
        <div style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; border-radius: 8px;">
            <h2 style="color: #2f80ed;">Thank You for Contacting Me</h2>
            <p>Hi {name},</p>
            <p>Thank you for reaching out! I have received your message and will get back to you shortly.</p>
            <p>Best regards,<br>Your Name / Company</p>
        </div>
        """

        request.env['mail.mail'].sudo().create({
            'subject': 'Thank you for contacting me',
            'body_html': body_html_auto_reply,
            'email_from': email_to,  
            'email_to': email_from,  
        }).send()

        # Save record in your model
        request.env['portfolio.contact.me'].sudo().create(vals)

        return Response("Thank you for contacting me!", status=200, mimetype='text/plain')

    
    #Fetches published repos
    def _get_repos_and_tags(self):
        repos = request.env['portfolio.repository'].sudo().search([('published', '=', True)])
        repo_list = []
        all_tags = set()

        for i, repo in enumerate(repos, 1):
            tag_names = [tag.name for tag in repo.portfolio_tag_ids]
            repo_list.append({
                'name': repo.name,
                'html_url': repo.url,
                'description': repo.description,
                'index': i,
                'tags': tag_names,
            })
            all_tags.update(tag_names)

        return repo_list, list(all_tags)
    

