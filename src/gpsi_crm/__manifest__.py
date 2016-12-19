# -*- coding: utf-8 -*-
{
    'name': 'GPSI CRM',
    'version': '1.0.0',
    'category': 'GPSI',
    'sequence': 20,
    'summary': 'CRM Extension',
    'description': '',
    'website': 'http://www.globalstd.com/',
    'depends': ['crm', 'mail', 'gpsi_project'],
    'data': [
        'security/crm_security.xml',
        'views/crm_views.xml',
        'data/crm_data.xml',
        'data/crm_workflow.xml',
        'data/crm_auto_actions.xml'
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
