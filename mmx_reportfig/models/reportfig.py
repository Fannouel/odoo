# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
#import logging
#_logger = logging.getLogger(__name__)
class Reportfig(models.Model):
    _name = "reportfig.reportfig"
    _description = "reportfig.reportfig"

    employee_id = fields.Many2one("hr.employee", string=_("Employee"))
    qty = fields.Float("Quantite produit", store=True)
    date = fields.Date(string=_("Date"))
    production_id = fields.Many2one("mrp.production", string=_("Production"))
    product_id = fields.Many2one("product.product", string=_("Product"), related="production_id.product_id", store=True)
    sale_order_id = fields.Many2one("sale.order", string=_("Sale Order"), related="production_id.sale_order_id")
    workcenter_id = fields.Many2one("mrp.workcenter", string=_("Work Center"), store=True)
    result = fields.Float(string="Quantite*Coef", store=True, compute='_compute_result', readonly=True)
    partner_id = fields.Many2one("res.partner", string=_("Partner"), related="sale_order_id.partner_id")
    dateDebut = fields.Date(string="Date Debut")
    dateFin = fields.Date(string="Date Fin")
    Urgence = fields.Selection(
        string="Urgence", related="production_id.state_fabric", readonly=True
    )
    product_qty = fields.Float(
        string=_("Production Quantity"), related="production_id.product_qty"
    )
    state_fabric = fields.Selection(
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

    numero_de_fiche = fields.Integer(string="Fiche numero")
    
    ######################## 
    # Champ séquentiel pour contrôler l'ordre des étapes
    
    completed_fonderie = fields.Boolean(string="Fonderie complétée", default=False)
    completed_ebarbage = fields.Boolean(string="Ebarbage complété", default=False)
    completed_soudure = fields.Boolean(string="Soudure complétée", default=False)
    completed_souscouche = fields.Boolean(string="Souscouche complétée", default=False)
    completed_peinture = fields.Boolean(string="Peinture complétée", default=False)
    
    # fonction qui fait la caclul des coef des article avec la Qtt produite
    
    @api.onchange("qty")
    def _onchange_qty(self):
        if self.workcenter_id and self.product_id:
            self._compute_result()

    @api.depends("workcenter_id", "product_id")
    def _compute_result(self):
        for record in self:
            if record.qty and record.workcenter_id and record.product_id:
                coefficient = 0.0  # Default coefficient value
                if record.workcenter_id.name == "FONDERIE":
                    coefficient = record.product_id.z_fonderie
                elif record.workcenter_id.name == "EBARBAGE":
                    coefficient = record.product_id.z_ebarbage
                elif record.workcenter_id.name == "SOUDURE":
                    coefficient = record.product_id.z_soudure
                elif record.workcenter_id.name == "SOUSCOUCHE":
                    coefficient = record.product_id.z_souscouche
                elif record.workcenter_id.name == "PEINTRE":
                    coefficient = record.product_id.z_peinture

                if coefficient == 0.0:
                    raise ValidationError(_("Pas de coefficient trouvé, veuillez définir un coefficient pour l'article."))
            
                record.result = record.qty * coefficient


    # fonction qui calclul le nombre de fiche 
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

    # verification saisi quantite produit

    @api.constrains('qty', 'product_qty')
    def check_qty(self):
        for record in self:
            if record.qty > record.product_qty:
                raise ValidationError(_("ERREUR DE SAISIE: Quantite Produite ne doit pas être supérieure à la quantité commandée."))

    # verification si numero de fiche existe

    @api.constrains('numero_de_fiche', 'production_id')
    def _check_duplicate_fiche_number(self):
        for record in self:
            if record.numero_de_fiche and record.production_id:
                existing_record = self.search([
                    ('numero_de_fiche', '=', record.numero_de_fiche),
                    ('production_id', '=', record.production_id.id),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_record:
                    raise ValidationError("Fiche déjà enregistrée pour cette production.")
    
    ############  verification etape de saisie 
    
    # Autres champs et méthodes
  
    @api.onchange('workcenter_id')
    def _onchange_workcenter_id(self):
        if self.workcenter_id.name == 'FONDERIE':
            self.completed_fonderie = True
            self.completed_ebarbage = False
            self.completed_soudure = False
            self.completed_souscouche = False
            self.completed_peinture = False
        elif self.workcenter_id.name == 'EBARBAGE':
            if not self.completed_fonderie:
                raise ValidationError(_("Veuillez compléter l'étape FONDERIE avant de passer à cette étape."))
            self.completed_ebarbage = True
            self.completed_soudure = False
            self.completed_souscouche = False
            self.completed_peinture = False
        elif self.workcenter_id.name == 'SOUDURE':
            if not self.completed_fonderie or not self.completed_ebarbage:
                raise ValidationError(_("Veuillez compléter les étapes précédentes avant de passer à SOUDURE."))
            self.completed_soudure = True
            self.completed_souscouche = False
            self.completed_peinture = False
        elif self.workcenter_id.name == 'SOUSCOUCHE':
            if not self.completed_fonderie or not self.completed_ebarbage or not self.completed_soudure:
                raise ValidationError(_("Veuillez compléter les étapes précédentes avant de passer à SOUSCOUCHE."))
            self.completed_souscouche = True
            self.completed_peinture = False
        elif self.workcenter_id.name == 'PEINTRE':
            if not self.completed_fonderie or not self.completed_ebarbage or not self.completed_soudure or not self.completed_souscouche:
                raise ValidationError(_("Veuillez compléter les étapes précédentes avant de passer à PEINTURE."))
            self.completed_peinture = True
   
        
        





    


