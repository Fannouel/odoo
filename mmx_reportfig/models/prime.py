# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Prime(models.Model):
    _name = "prime.prod"

    prod_nb = fields.Float(string="Qtt Article Produit")
    date = fields.Date(string="Mois")
    prime_amount = fields.Float(
        string="Prime(Ar)", compute="_compute_prime", store=True
    )
    sbh = fields.Float(
        string="Salaire de base par heure (Ar)", compute="_compute_sbh", store=True
    )
    contract_id = fields.Many2one("hr.contract", string="Employé", required=True)

    @api.depends("contract_id.wage")
    def _compute_sbh(self):
        for contract in self:
            if contract.contract_id.wage:
                contract.sbh = contract.contract_id.wage / 160.0
            else:
                contract.sbh = 0.0

    @api.depends("sbh", "prod_nb", "contract_id.wage")
    def _compute_prime(self):
        for contract in self:
            prime = (contract.prod_nb * contract.sbh) - contract.contract_id.wage
            contract.prime_amount = max(prime, 0.0)
