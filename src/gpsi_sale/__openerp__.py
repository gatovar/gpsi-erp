# -*- coding: utf-8 -*-
{
    'name': 'GPSI Sales',
    'version': '1.0.0',
    'category': 'globalstd',
    'sequence': 20,
    'summary': 'Sales Extension',
    'description': '',
    'website': 'http://www.globalstd.com/',
    'depends': ['mail','sale'],
    'data': [
        'views/sale_views.xml',
        'views/contract_views.xml',
        'data/sale_data.xml'
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
