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
            'my_portfolio/static/src/js/carousel_out_of_bound_fix'
            
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/portfolio_menu.xml',
        'views/portfolio_github_wizard_view.xml',
        'views/portfolio_carousel_view.xml',
        'views/portfolio_admin_publish_view.xml',
        
        
        
    ],
    
}