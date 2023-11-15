# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models, _
import requests
from odoo.exceptions import ValidationError, UserError
import json


class ResUsers(models.Model):
    _inherit = "res.users"

    trello_api_key = fields.Char(string="Trello API Key")
    trello_api_token = fields.Char(string="Trello API Token")
    trello_username = fields.Char(string="Trello User Name")
    trello_user_id = fields.Char(string="Trello User ID", readonly=True, copy=False)

    def get_trello_api_key(self):
        url_action = {
            "type": "ir.actions.act_url",
            "name": "Trello API Key",
            "target": "new",
            "url": "https://trello.com/app-key",
        }
        return url_action

    def get_trello_api_token(self):
        api_key = self.trello_api_key
        url_action = {
            "type": "ir.actions.act_url",
            "name": "Trello API Token",
            "target": "new",
            "url": "https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server%20Token&key="
            + api_key,
        }
        return url_action

    def test_url(self):
        if self.trello_api_key and self.trello_api_token and self.trello_username:
            url = "https://api.trello.com/1/members/" + self.trello_username
            querystring = {"key": self.trello_api_key, "token": self.trello_api_token}
            response = requests.request("GET", url, params=querystring)
            datas = json.loads(response.text)
            if response.text == "invalid key":
                raise ValidationError(_("Invalid Key"))
            elif response.text == "invalid token":
                raise ValidationError(_("Invalid Token"))
            else:
                self.trello_user_id = datas["id"]
            return {
                "name": "Success Message",
                "type": "ir.actions.act_window",
                "res_model": "success.wizard",
                "view_mode": "form",
                "view_type": "form",
                "target": "new",
            }

    def sync_with_trello(self):
        if self.trello_user_id:
            trello_data = self.env["trello.data"]
            trello_data.get_trello_projects()
            trello_data.get_trello_stages()
            trello_data.get_trello_cards()
            trello_data.sync_datas_to_trello()
            return {
                "name": "Success Message",
                "type": "ir.actions.act_window",
                "res_model": "sync.wizard",
                "view_mode": "form",
                "view_type": "form",
                "target": "new",
            }

    def automated_sync_with_trello(self):
        users = self.env["res.users"].search([])
        for user in users:
            if user and user.trello_user_id:
                trello_data = self.env["trello.data"]
                trello_data.get_trello_projects(user)
                trello_data.get_trello_stages(user)
                trello_data.get_trello_cards(user)
                trello_data.sync_datas_to_trello(user)
