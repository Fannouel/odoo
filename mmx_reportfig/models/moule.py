
from odoo import models, fields

class Moule(models.Model):
    _name = "moule.product"
    numero_moule = fields.Char(string="Numero de Moule")
    product_line_ids = fields.One2many("product.template.line", "moule_id", string="Lignes de Produits")
    # Définir la méthode display_name pour afficher le numéro de moule
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.numero_moule))
        return res

class ProductTemplateLine(models.Model):
    _name = "product.template.line"
    product_id = fields.Many2one("product.product", string="Produit")
    moule_id = fields.Many2one("moule.product", string="Numéro de Moule")
    template_id = fields.Many2one("product.template", string="Template ID")


class TypeMoule(models.Model):
    _inherit = "product.template"
    product_line_ids = fields.One2many("product.template.line", "template_id", string="Lignes de Produits")
    tete_id = fields.Many2one("moule.product", string="tête")
    corp_id = fields.Many2one("moule.product", string="corps")
    sacdos_id = fields.Many2one("moule.product", string="sac à dos")
    petitecanne_id = fields.Many2one("moule.product", string="petite canne")
    product_id = fields.Many2one("product.product", string="Produit")
    moule_id = fields.Many2one("moule.product", string="Numéro de Moule")
    
    def action_add_product_line(self):
            self.ensure_one()
            self.product_line_ids = [(0, 0, {
                "product_id": False,
                "moule_id": self.moule_id.id,
                "template_id": self.id,
            })]