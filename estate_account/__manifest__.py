# -*- coding: utf-8 -*-

{
    'name' : 'Real Estate Accounting',
    'version' : '17.0',
    'summary': 'Real Estate Accounting Management Software',
    'sequence': -1,
    'description': """Real Estate Accounting Management Software""",
    'category': 'Real Estate',
    'website': 'https://www.odoomates.tech',
    'license':'LGPL-3',
    'depends' : ['base', 'estate', 'account'],
    'data': [

        'security/ir.model.access.csv',
        # 'views/estate_property_views.xml',
        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
