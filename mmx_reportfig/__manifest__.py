# -*- coding: utf-8 -*-
{
    "name": "mmx_reportfig",
    "summary": """
        add menu report et suivie commande dans model fabrication""",
    "description": """
        add menu report et suivie commande dans model fabrication
    """,
    "author": "tanjona",
    "website": "minimad.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "fabrication",
    "version": "16.0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "excel_import_export",
        "hr",
        "mrp",
        "sale_management",
        "product",
        "hr_contract",
        "account",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/templates.xml",
        "views/reportfig.xml",
        "views/mrp_production.xml",
        "views/product_template.xml",
        "export/actions.xml",
        "export/templates.xml",
        "views/prime.xml",
        "views/account_move_line.xml",
        "wizard/order_follow_up.xml",
        "views/moule.xml",
        "views/report_pivot.xml",
        #"views/reportfig_workflow.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
