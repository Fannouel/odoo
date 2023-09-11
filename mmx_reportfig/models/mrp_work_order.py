# -*- coding: utf-8 -*-
from odoo import models, fields


class MrpWorkOrder(models.Model):
    _inherit = "mrp.workorder"

    employee_id = fields.Many2one("hr_employee", string="Employee")
