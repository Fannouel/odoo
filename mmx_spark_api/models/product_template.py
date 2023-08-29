from odoo import models, fields


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    erpdev_id = fields.Char(string="Dev ERP Id")
