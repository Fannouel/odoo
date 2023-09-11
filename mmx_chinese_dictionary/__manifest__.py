# -*- coding: utf-8 -*-
{
    "name": "MMX chinese dictionary",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "ANDRIANJAFIMALALA H. Fanoela",
    "website": "https://www.sparkmodel.com.com",
    "category": "Tools",
    "version": "0.1",
    "depends": ["excel_import_export", "base"],
    "data": [
        "security/ir.model.access.csv",
        "views/chinese_dico.xml",
        "views/menu.xml",
    ],
    "installable": True, 
}
