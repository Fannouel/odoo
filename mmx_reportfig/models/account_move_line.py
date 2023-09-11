# -*- coding: utf-8 -*-

# la classe accountMoveLine ajout le numero de bon de command dans la facture
from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    orderform_number = fields.Char(
        string="Order Form Number", compute="_compute_orderform_number", readonly=True
    )

    def _compute_orderform_number(self):
        """Compute order forn number separating them by commas."""
        for line in self:
            order_numbers = []
            for sale_line in line.sale_line_ids:
                if sale_line.order_id.name:
                    order_numbers.append(sale_line.order_id.name)
            line.orderform_number = ", ".join(order_numbers)
