# -*- coding: utf-8 -*-
from odoo import models, fields


class CustomMrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"

    empl_id = fields.Many2one("hr_employee", string="Employee")
