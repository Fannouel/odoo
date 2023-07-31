# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class pour le calcule de coeffitient

class BCFig(models.Model):
     _inherit = 'mrp.production'
     BC = fields.Many2one('sale.order', string='Bon de Commande')
     stateFabric = fields.Selection([('U', 'Urgent'), ('M', 'Moyenne'), ('B', 'Basse')], string='Priorité', store=True)
     client = fields.Many2one('res.partner', string='Client')

