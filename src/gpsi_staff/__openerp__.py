# -*- coding: utf-8 -*-
{
    'name': 'GPSI Staff',
    'version': '0.0.1',
    'category': 'gpsi',
    'sequence': 20,
    'summary': 'Audit Management',
    'description': '',
    'website': '',
    'depends': ['mail', 'project', 'project_issue'],
    'data': [
        'data/staff_audit_data.xml',
        'views/staff_views.xml',
        'views/staff_audit_views.xml',
        'views/staff_audit_website.xml',
        'reports/audit_reports.xml'
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True
}
