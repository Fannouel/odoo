# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Reportfig(models.Model):
    _name = "reportfig.reportfig"
    _description = "reportfig.reportfig"

    employee_id = fields.Many2one("hr.employee", string=_("Employee"))
    qty = fields.Float("Quantite produit", store=True)
    date = fields.Date(string=_("Date"))
    production_id = fields.Many2one("mrp.production", string=_("Production"))
    product_id = fields.Many2one("product.product", string=_("Product"), related="production_id.product_id", store=True)
    sale_order_id = fields.Many2one("sale.order", string=_("Sale Order"), related="production_id.sale_order_id")
    workcenter_id = fields.Many2one("mrp.workcenter", string=_("Work Center"))
    result = fields.Float(string="Quantite*Coef", store=True)
    partner_id = fields.Many2one("res.partner", string=_("Partner"), related="sale_order_id.partner_id")
    dateDebut = fields.Date(string="Date Debut")
    dateFin = fields.Date(string="Date Fin")
    Urgence = fields.Selection(
        string="Urgence", related="production_id.state_fabric", readonly=True
    )
    product_qty = fields.Float(
        string=_("Production Quantity"), related="production_id.product_qty"
    )
    state = fields.Selection(
        [("L", "Lancé en Fabrication"), ("A", "en attente"), ("T", "Términé")],
        string="state Fabric",
        store=True,
    )
    quota = fields.Integer(string="quota")
    NbrDeFiche = fields.Integer(
        string="Nbr de Fiche", compute="_nbrfiche", store="True"
    )
    ResteFiche = fields.Integer(
        string="Reste Article", compute="_restfiche", store="True"
    )

    # fonction qui caclul le coefficient des article
    @api.onchange("workcenter_id", "product_id")
    def _onchange_post_de_travail_product_id(self):
        if self.workcenter_id and self.product_id:
            if self.workcenter_id.name == "FFONDERIE":
                self.result = self.qty * self.product_id.z_fonderie
            elif self.workcenter_id.name == "EBARBAGE":
                self.result = self.qty * self.product_id.z_ebarbage
            elif self.workcenter_id.name == "SOUDURE":
                self.result = self.qty * self.product_id.z_soudure
            elif self.workcenter_id.name == "SOUSCOUCHE":
                self.result = self.qty * self.product_id.z_souscouche
            elif self.workcenter_id.name == "PEINTRE":
                self.result = self.qty * self.product_id.z_peinture
            else:
                self.result = 0.0

    # fonction qui calcul le nomb
    # re de fiche avec reste
    @api.depends("product_qty", "quota")
    def _nbrfiche(self):
        for record in self:
            if record.quota != 0:
                record.NbrDeFiche = record.product_qty // record.quota
            else:
                record.NbrDeFiche = 0

    @api.depends("product_qty", "quota")
    def _restfiche(self):
        for record in self:
            if record.quota != 0:
                record.ResteFiche = record.product_qty % record.quota
            else:
                record.ResteFiche = 0
