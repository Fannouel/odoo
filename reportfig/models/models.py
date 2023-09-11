# -*- coding: utf-8 -*-

from odoo import models, fields, api


# from odoo.addons.reportfig.models.coef import fonderie
class reportfig(models.Model):
    _name = "reportfig.reportfig"
    _description = "reportfig.reportfig"

    name_id = fields.Many2one("hr.employee", string="Travalleur")
    postDeTravail_id = fields.Many2one("mrp.workcenter", "post de travail")
    QuantitePrd = fields.Float("Quantite produit", store=True)
    dateAddProd = fields.Date(string="Date Print Fiche", format="%d/%m/%Y")
    art_id = fields.Many2one("product.product", string="Article", store=True)
    origin = fields.Char(
        string="N°Bon Command", related="NFabric_id.BC.name", readonly=True
    )
    NFabric_id = fields.Many2one("mrp.production", string="N°Ordre Fabrication")
    result = fields.Float(string="Quantite*Coef", store=True)
    client = fields.Many2one("res.partner", string="Client")
    dateDebut = fields.Date(string="Date Debut")
    dateFin = fields.Date(string="Date Fin")
    Urgence = fields.Selection(
        string="Urgence", related="NFabric_id.stateFabric", readonly=True
    )
    QttCommander = fields.Float(
        string="Quantite Command", related="NFabric_id.product_qty"
    )
    Etat = fields.Selection(
        [("L", "Lancé en Fabrication"), ("A", "en attente"), ("T", "Términé")],
        string="Etat Fabric",
        store=True,
    )
    Quotat = fields.Integer(string="Quotat")
    NbrDeFiche = fields.Integer(
        string="Nbr de Fiche", compute="_nbrfiche", store="True"
    )
    ResteFiche = fields.Integer(
        string="Reste Article", compute="_restfiche", store="True"
    )

    # fonction qui caclul le coefficient des article
    @api.onchange("postDeTravail_id", "art_id")
    def _onchange_post_de_travail_art_id(self):
        if self.postDeTravail_id and self.art_id:
            if self.postDeTravail_id.name == "FONDEUR":
                self.result = self.QuantitePrd * self.art_id.z_fonderie
            elif self.postDeTravail_id.name == "EBARBEUR":
                self.result = self.QuantitePrd * self.art_id.z_ebarbage
            elif self.postDeTravail_id.name == "SOUDEUR":
                self.result = self.QuantitePrd * self.art_id.z_soudure
            elif self.postDeTravail_id.name == "SOUSCOUCHE":
                self.result = self.QuantitePrd * self.art_id.z_souscouche
            elif self.postDeTravail_id.name == "PEINTRE":
                self.result = self.QuantitePrd * self.art_id.z_peinture
            else:
                self.result = 0.0

    # fonction qui calcul le nombre de fiche avec reste
    @api.depends("QttCommander", "Quotat")
    def _nbrfiche(self):
        for record in self:
            if record.Quotat != 0:
                record.NbrDeFiche = record.QttCommander // record.Quotat
            else:
                record.NbrDeFiche = 0

    @api.depends("QttCommander", "Quotat")
    def _restfiche(self):
        for record in self:
            if record.Quotat != 0:
                record.ResteFiche = record.QttCommander % record.Quotat
            else:
                record.ResteFiche = 0
