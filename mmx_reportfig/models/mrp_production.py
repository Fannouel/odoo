# -*- coding: utf-8 -*-

# la classe MrpProduction ajout un champ numero BC, status de fabtication et client
from odoo import models, fields, _

""" Inherit MRP Production to add fields
"""


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    state_fabric = fields.Selection(
        [(_("U"), "Urgent"), (_("N"), "Normal"), (_("L"), "Low")],
        string=_("Priority"),
        store=True,
    )
    sale_order_line_id = fields.Many2one("sale.order.line", string=_("Sale Order Line"))
    sale_order_id = fields.Many2one(
        "sale.order", string=_("Sale Order"), related="sale_order_line_id.order_id")
    partner_id = fields.Many2one(
        "res.partner", string=_("Client"), related="sale_order_id.partner_id")
