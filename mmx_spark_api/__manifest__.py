# -*- coding: utf-8 -*-
{
    "name": "spark_api",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "ANDRIANJAFIMALALA H. Fanoela",
    "website": "https://www.sparkmodel.com.com",
    "category": "Fabrication",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "product"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/product_template.xml"
    ],
}
