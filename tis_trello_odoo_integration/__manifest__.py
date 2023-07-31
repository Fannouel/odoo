# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

{
    'name': 'Trello - Odoo Integration',
    'version': '14.0.0.2',
    'category': 'Project',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'By-directional sync between Trello & Odoo',
    'website': 'http://www.technaureus.com/',
    'price': 69.99,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'description': """ 
    Integrating Trello with Odoo and managing tasks from Trello in Odoo.
""",
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/res_users_views.xml',
        'views/project_views.xml',
        'wizard/notification_wizard_view.xml',
    ],
    'demo': [
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
