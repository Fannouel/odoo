# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models
import requests
import json
import re

TAG_RE = re.compile(r'<[^>]+>')


class Project(models.Model):
    _inherit = "project.project"

    trello_project_id = fields.Char(string='Trello Project ID', copy=False)
    last_sync_at = fields.Datetime(string='Last Synced With Trello At')

    def unlink(self):
        if self.trello_project_id:
            url = "https://api.trello.com/1/boards/" + self.trello_project_id
            querystring = {"key": self.env.user.trello_api_key, "token": self.env.user.trello_api_token}
            requests.request("DELETE", url, params=querystring)
        return super(Project, self).unlink()

    def sync_project_to_trello(self):
        api_key = self.env.user.trello_api_key
        api_token = self.env.user.trello_api_token
        if self.env.user.trello_user_id:
            for project in self:
                for task in project.task_ids:
                    if project.trello_project_id:
                        project_url = "https://api.trello.com/1/boards/" + project.trello_project_id
                        project_querystring = {"name": project.name,
                                               "closed": "true" if project.active == False else "false",
                                               "key": api_key, "token": api_token}
                        project_response = requests.request("PUT", project_url, params=project_querystring)
                        if project_response:
                            project_response_datas = json.loads(project_response.text)
                            project.trello_project_id = project_response_datas['id']
                        project.sync_stages_to_trello()
                        task.sync_task_to_trello()
                    else:
                        project_url = "https://api.trello.com/1/boards/"
                        project_querystring = {"name": project.name, "defaultLists": "false",
                                               "closed": "true" if project.active == False else "false",
                                               "key": api_key, "token": api_token}
                        project_response = requests.request("POST", project_url, params=project_querystring)
                        if project_response:
                            project_response_datas = json.loads(project_response.text)
                            project.trello_project_id = project_response_datas['id']
                        project.sync_stages_to_trello()
                        task.sync_task_to_trello()
                project.last_sync_at = fields.Datetime.now()

    def sync_stages_to_trello(self):
        api_key = self.env.user.trello_api_key
        api_token = self.env.user.trello_api_token
        for stages in self.type_ids:
            if stages.trello_stage_id:
                stage_url = "https://api.trello.com/1/lists/" + stages.trello_stage_id
                stage_querystring = {"name": stages.name, "pos": "bottom", "idBoard": self.trello_project_id,
                                     "key": api_key, "token": api_token}
                stage_response = requests.request("PUT", stage_url, params=stage_querystring)
            else:
                stage_url = "https://api.trello.com/1/lists"
                stage_querystring = {"name": stages.name, "pos": "bottom", "idBoard": self.trello_project_id,
                                     "key": api_key, "token": api_token}
                stage_response = requests.request("POST", stage_url, params=stage_querystring)
            if stage_response:
                stage_response_datas = json.loads(stage_response.text)
                stages.trello_stage_id = stage_response_datas['id']


class ProjectTask(models.Model):
    _inherit = "project.task"

    trello_task_id = fields.Char(string='Trello Task ID', copy=False)
    last_sync_at = fields.Datetime(string='Last Synced With Trello At')

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if vals.get('active') == False:
            self.sync_task_to_trello()
        return res

    def unlink(self):
        if self.trello_task_id:
            url = "https://api.trello.com/1/cards/" + self.trello_task_id
            querystring = {"key": self.env.user.trello_api_key, "token": self.env.user.trello_api_token}
            requests.request("DELETE", url, params=querystring)
        return super(ProjectTask, self).unlink()

    def sync_task_to_trello(self):
        api_key = self.env.user.trello_api_key
        api_token = self.env.user.trello_api_token
        if self.env.user.trello_user_id:
            for task in self:
                label_list = []
                for tag in task.tag_ids:
                    if tag.color == '':
                        color = 'null'
                    elif tag.color == 1:
                        color = 'red'
                    elif tag.color == 2:
                        color = 'orange'
                    elif tag.color == 3:
                        color = 'yellow'
                    elif tag.color == 4:
                        color = 'sky'
                    elif tag.color == 5:
                        color = 'null'
                    elif tag.color == 6:
                        color = 'pink'
                    elif tag.color == 7:
                        color = 'null'
                    elif tag.color == 8:
                        color = 'blue'
                    elif tag.color == 9:
                        color = 'null'
                    elif tag.color == 10:
                        color = 'green'
                    elif tag.color == 11:
                        color = 'purple'
                    else:
                        color = ''
                    if tag.trello_tag_id:
                        tag_url = "https://api.trello.com/1/labels/" + tag.trello_tag_id
                        tag_querystring = {"name": tag.name, "color": color, "key": api_key, "token": api_token}
                        tag_response = requests.request("PUT", tag_url, params=tag_querystring)
                    else:
                        tag_url = "https://api.trello.com/1/labels"
                        tag_querystring = {"name": tag.name, "color": color,
                                           "idBoard": task.project_id.trello_project_id,
                                           "key": api_key, "token": api_token}
                        tag_response = requests.request("POST", tag_url, params=tag_querystring)
                    if tag_response:
                        tag_response_datas = json.loads(tag_response.text)
                        tag.trello_tag_id = tag_response_datas['id']
                        label_list.append(tag.trello_tag_id)
                if task.trello_task_id:
                    task.project_id.sync_stages_to_trello()
                    task_url = "https://api.trello.com/1/cards/" + task.trello_task_id
                    task_querystring = {"idList": task.stage_id.trello_stage_id, "name": task.name,
                                        "pos": task.sequence,
                                        "desc": TAG_RE.sub('', task.description) if task.description else '',
                                        "due": task.date_deadline if task.date_deadline else '',
                                        "keepFromSource": "all", "idLabels": label_list,
                                        "closed": "true" if task.active == False else "false",
                                        "key": api_key, "token": api_token}
                    task_response = requests.request("PUT", task_url, params=task_querystring)
                else:
                    if not task.project_id.trello_project_id:
                        project_url = "https://api.trello.com/1/boards/"
                        project_querystring = {"name": task.project_id.name,
                                               "defaultLists": "false",
                                               "closed": "true" if task.project_id.active == False else "false",
                                               "key": api_key,
                                               "token": api_token}
                        project_response = requests.request("POST",
                                                            project_url,
                                                            params=project_querystring)
                        if project_response:
                            project_response_datas = json.loads(
                                project_response.text)
                            task.project_id.trello_project_id = project_response_datas[
                                'id']
                    task.project_id.sync_stages_to_trello()
                    task_url = "https://api.trello.com/1/cards"
                    task_querystring = {"idList": task.stage_id.trello_stage_id, "name": task.name,
                                        "pos": task.sequence,
                                        "desc": TAG_RE.sub('', task.description) if task.description else '',
                                        "due": task.date_deadline if task.date_deadline else '',
                                        "keepFromSource": "all", "idLabels": label_list,
                                        "closed": "true" if task.active == False else "false",
                                        "key": api_key, "token": api_token}
                    task_response = requests.request("POST", task_url, params=task_querystring)
                if task_response:
                    task_response_datas = json.loads(task_response.text)
                    task.trello_task_id = task_response_datas['id']
                    task.last_sync_at = fields.Datetime.now()
                for attachment in task.attachment_ids:
                    if not attachment.trello_attachment_id:
                        file_path = attachment._full_path(attachment.store_fname)
                        attachment_url = "https://api.trello.com/1/cards/" + task.trello_task_id + "/attachments"
                        attachment_querystring = {"key": api_key, "token": api_token, "name": attachment.name}
                        files = {'file': open(file_path, 'rb')}
                        attachment_response = requests.request("POST", attachment_url,
                                                               params=attachment_querystring,
                                                               files=files)
                        if attachment_response:
                            attachment_datas = json.loads(attachment_response.text)
                            attachment.trello_attachment_id = attachment_datas['id']


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    trello_stage_id = fields.Char(string='Trello Stage ID', copy=False)


class ProjectTags(models.Model):
    _inherit = "project.tags"

    trello_tag_id = fields.Char(string='Trello Tag ID', copy=False)
    project_id = fields.Many2one('project.project', string='Project', required=True, copy=False)
    _sql_constraints = [
        ('name_uniq', 'unique (name, project_id, color)', "Tag name already exists"),
    ]
