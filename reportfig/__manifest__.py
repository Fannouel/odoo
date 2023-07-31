# -*- coding: utf-8 -*-
{
    'name': "reportfig",

    'summary': """
        add menu report dans model fabrication""",

    'description': """
        add menu report dans model fabrication
    """,

    'author': "min",
    'website': "sparkmodel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'fabrication',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['excel_import_export',
				'report_xlsx',
				'base',
				'hr',
				'mrp',
				'sale',
				'product',
				'hr_contract',
				'account',
				],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/reportfig.xml',
        'views/BC.xml',
        'views/coef.xml',
        'export/actions.xml',
        'export/templates.xml',
        'views/prime.xml',
		'views/NUMBC.xml',
#		'views/empl.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
