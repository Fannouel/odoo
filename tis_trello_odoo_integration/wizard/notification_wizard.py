# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models


class SuccessWizard(models.TransientModel):
    _name = "success.wizard"


class SyncWizard(models.TransientModel):
    _name = "sync.wizard"
