# Copyright 2013-2020 Open2Bizz <info@open2bizz.nl>
# License LGPL-3

{
    'name': 'crm_exp_revenue_hours',
    'summary': 'CRM Addon to set expected revenue in Hours',
    'version': '12.0.1.0.0',
    'category': 'Customer Relationship Management',
    'website': 'https://www.open2bizz.nl/',
    'author': 'Open2Bizz',
    'license': 'LGPL-3',
    'installable': True,
    'depends': [
        'crm',
    ],
    'data': ['views/crm_lead_view.xml'],
}
