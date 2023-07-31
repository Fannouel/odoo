# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class pour le calcule de coeffitient
class coef(models.Model):

    _inherit = 'product.template'

    # variable fonderie
    x_fonderie = fields.Float(string='coef_fonderie(/)')
    y_fonderie = fields.Float(string='.')
    z_fonderie = fields.Float(string='Z Fonderie', store=True, compute='_fonderie')

    # variable ebarbage
    x_ebarbage = fields.Float(string='coef_ebarbage(/)')
    y_ebarbage = fields.Float(string='.')
    z_ebarbage = fields.Float(string='Z Ebarbage', store=True, compute='_ebarbage')

    # variable soudure
    x_soudure = fields.Float(string='coef_soudure(/)')
    y_soudure = fields.Float(string='.')
    z_soudure = fields.Float(string='z', store=True, compute='_soudure')

    # variable souscouche
    x_souscouche = fields.Float(string='coef_souscouche(/)')
    y_souscouche = fields.Float(string='.')
    z_souscouche = fields.Float(string='z', store=True, compute='_souscouche')
    # fonction qui calcul la coef du fonderie

    # variable peinture
    x_peinture = fields.Float(string='coef_peinture(/)')
    y_peinture = fields.Float(string='.')
    z_peinture = fields.Float(string='z', store=True, compute='_peinture')


    # fonction qui calcul la coef du fonderie
    @api.depends('x_fonderie','y_fonderie','z_fonderie')
    def _fonderie(self):
        for record in self:
            if record.y_fonderie != 0:
                record.z_fonderie = record.x_fonderie / record.y_fonderie
            else:
                record.z_fonderie = 0

    # fonction qui calcul la coef du ebarbage
    @api.depends('x_ebarbage', 'y_ebarbage','z_ebarbage')
    def _ebarbage(self):
        for record in self:
            if record.y_ebarbage != 0:
                record.z_ebarbage = record.x_ebarbage / record.y_ebarbage
            else:
                record.z_ebarbage = 0

    # fonction qui calcul la coef du soudure
    @api.depends('x_soudure', 'y_soudure', 'z_soudure')
    def _soudure(self):
        for record in self:
            if record.y_soudure != 0:
                record.z_soudure = record.x_soudure / record.y_soudure
            else:
                record.z_soudure = 0

    # fonction qui calcul la coef du souscouche
    @api.depends('x_souscouche', 'y_souscouche', 'z_souscouche')
    def _souscouche(self):
        for record in self:
            if record.y_souscouche != 0:
                record.z_souscouche = record.x_souscouche / record.y_souscouche
            else:
                record.z_souscouche = 0

    # fonction qui calcul la coef du peinture
    @api.depends('x_peinture', 'y_peinture', 'z_peinture')
    def _peinture(self):
        for record in self:
            if record.y_peinture != 0:
                record.z_peinture = record.x_peinture / record.y_peinture
            else:
                record.z_peinture = 0


