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
    workcenter_id = fields.Many2one("mrp.workcenter", string=_("Work Center"))
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
    
    """    
    last_completed_step = fields.Selection(
        [("FONDERIE", "FONDERIE"), ("EBARBAGE", "EBARBAGE"), ("SOUDURE", "SOUDURE"), ("SOUSCOUCHE", "SOUSCOUCHE"), ("PEINTRE", "PEINTRE")],
        string="Dernière étape complétée",
        default="FONDERIE",
        compute="_check_workcenter_order",
        store=True,
    )
    
    # ajout champ boolen
    completed_fonderie = fields.Boolean(string="Fonderie complétée", default=False)
    completed_ebarbage = fields.Boolean(string="Ebarbage complété", default=False)
    completed_soudure = fields.Boolean(string="Soudure complétée", default=False)
    completed_souscouche = fields.Boolean(string="Souscouche complétée", default=False)
    completed_peintre = fields.Boolean(string="Peintre complété", default=False)
    """
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

    
    # Contrainte pour vérifier l'ordre des étapes
"""   
    @api.constrains('last_completed_step', 'workcenter_id')
    def _check_workcenter_order(self):
        for record in self:
            workcenter_order = {
                "FONDERIE": 1,
                "EBARBAGE": 2,
                "SOUDURE": 3,
                "SOUSCOUCHE": 4,
                "PEINTRE": 5,
            }

            current_step = record.workcenter_id.name
            last_completed_step = record.last_completed_step

            if current_step not in workcenter_order or last_completed_step not in workcenter_order:
                # Gérer le cas où une étape n'est pas définie dans le dictionnaire
                continue

            if current_step == "FONDERIE":
                if last_completed_step != "FONDERIE":
                    raise ValidationError(f"Fiche {current_step} ne peut pas être enregistrée. Étape incorrecte : {last_completed_step}")
            else:
                # Trouver la dernière étape complétée
                last_completed_step_order = workcenter_order[last_completed_step]

                # Vérifier si la nouvelle étape est la suivante dans l'ordre
                if workcenter_order[current_step] != last_completed_step_order + 1:
                    missing_steps = [step_name for step_name, step_order in workcenter_order.items() if step_order == last_completed_step_order + 1]
                    missing_step_names_str = ", ".join(missing_steps)
                    raise ValidationError(f"Fiche {current_step} peut pas être enregistré. une Étapes manquantes : {missing_step_names_str}")
    

    @api.constrains('last_completed_step', 'workcenter_id')
    def _check_workcenter_order(self):
        for record in self:
            workcenter_order = {
                "FONDERIE": 1,
                "EBARBAGE": 2,
                "SOUDURE": 3,
                "SOUSCOUCHE": 4,
                "PEINTRE": 5,
            }

            current_step = record.workcenter_id.name
            last_completed_step = record.last_completed_step

            if current_step not in workcenter_order or last_completed_step not in workcenter_order:
                # Gérer le cas où une étape n'est pas définie dans le dictionnaire
                continue

            if current_step == "FONDERIE":
                if last_completed_step != "FONDERIE":
                    raise ValidationError(f"Fiche {current_step} ne peut pas être enregistrée. Étape incorrecte : {last_completed_step}")
            else:
                # Trouver la dernière étape complétée
                last_completed_step_order = workcenter_order[last_completed_step]

                # Vérifier si la nouvelle étape est la suivante dans l'ordre
                if workcenter_order[current_step] != last_completed_step_order + 1:
                    missing_steps = [step_name for step_name, step_order in workcenter_order.items() if step_order == last_completed_step_order + 1]
                    missing_step_names_str = ", ".join(missing_steps)
                    raise ValidationError(f"Fiche {current_step} ne peut pas être enregistrée. Étape incorrecte : {last_completed_step}. Étapes manquantes : {missing_step_names_str}")
"""
    



    


