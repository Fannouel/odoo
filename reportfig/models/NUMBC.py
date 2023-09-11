# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomInvoice(models.Model):
    _inherit = "account.move"


class CustomInvoiceLine(models.Model):
    _inherit = "account.move.line"

    num_bon_commande_vente = fields.Char(
        string="Numéro_BC", compute="_compute_num_bon_commande_vente", readonly=True
    )

    def _compute_num_bon_commande_vente(self):
        for line in self:
            order_numbers = []
            for sale_line in line.sale_line_ids:
                if sale_line.order_id.name:
                    order_numbers.append(sale_line.order_id.name)
            line.num_bon_commande_vente = ", ".join(order_numbers)
