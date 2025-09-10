{
    'name': 'my portfolio',
    'version': '18.0.1.0.0',
    'depends': ['base','website'],
    'author': 'Anders',
    'category': 'My Portfolio',
    'description': 'website to display github portfolio',
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'my_portfolio/static/src/js/carousel_tag_filter.js',
            
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/portfolio_github_wizard_view.xml',
        'views/portfolio_about_me_backend_view.xml',
        'views/portfolio_about_me_partner_logo_view.xml',
        'views/portfolio_experience_card_backend_view.xml',
        'views/portfolio_about_me_card_tag_backend_view.xml',
        'views/portfolio_menu.xml',
        'views/portfolio_carousel_view.xml',
        'views/portfolio_publish_repo_view.xml', 
        'views/portfolio_about_me_frontend_view.xml',
        
    ],
    
}