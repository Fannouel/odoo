# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd. - ©
# Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.


from odoo import fields, api, models
import requests


class Attachment(models.Model):
    _inherit = "ir.attachment"

    trello_attachment_id = fields.Char(string='Trello Attachment ID', copy=False)

    def unlink(self):
        for attachment in self:
            if attachment.trello_attachment_id:
                task = self.env['project.task'].search([('id', '=', attachment.res_id)])
                if task.trello_task_id:
                    url = "https://api.trello.com/1/cards/" + task.trello_task_id + "/attachments/" + attachment.trello_attachment_id
                    querystring = {"key": self.env.user.trello_api_key, "token": self.env.user.trello_api_token}
                    requests.request("DELETE", url, params=querystring)
            return super(Attachment, self).unlink()
