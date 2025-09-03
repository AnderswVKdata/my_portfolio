{
    'name': 'my portfolio',
    'version': '18.0.1.0.0',
    'depends': ['website'],
    'author': 'Anders',
    'category': 'My Portfolio',
    'description': 'website to display github portfolio',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            
        ],
    },
    'data': [
        'views/portfolio_carousel_view.xml',
        'views/portfolio_aboutme_view.xml',
        'views/portfolio_contactme_view.xml',
        'views/portfolio_admin_publish_view.xml',
        
    ],
    
}