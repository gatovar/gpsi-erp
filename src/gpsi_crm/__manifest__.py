# -*- coding: utf-8 -*-
{
    'name': 'GPSI CRM',
    'version': '1.0.0',
    'category': 'GPSI',
    'sequence': 20,
    'summary': 'CRM Extension',
    'description': '',
    'website': 'http://www.globalstd.com/',
    'depends': ['crm', 'gpsi_project'],
    'data': [
        'views/crm_views.xml',
        'data/crm_data.xml'
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
