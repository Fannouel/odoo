# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import models, api, fields
import requests
import json
import re

TAG_RE = re.compile(r'<[^>]+>')


class TrelloData(models.Model):
    _name = "trello.data"
    _description = 'Trello Data'

    def get_trello_projects(self, user=None):
        project = self.env['project.project']
        project_data = {}
        if user or self.env.user:
            trello_username = user.trello_username if user and user.trello_username else self.env.user.trello_username
            trello_api_key = user.trello_api_key if user and user.trello_api_key else self.env.user.trello_api_key
            trello_api_token = user.trello_api_token if user and user.trello_api_token else self.env.user.trello_api_token
            if trello_username and trello_api_key and trello_api_token:
                url = "https://api.trello.com/1/members/" + trello_username + "/boards"
                querystring = {"lists": "all", "key": trello_api_key, "token": trello_api_token}
                response = requests.request("GET", url, params=querystring)
                print("response",response)
                if response:
                    datas = json.loads(response.text)
                    for data in datas:
                        stage_data = []
                        for stage in data['lists']:
                            stage_data.append(stage['name'])
                        project_data.update({data['id']: stage_data})
                        existing_project = project.search([('trello_project_id', '=', data['id'])])
                        if not existing_project:
                            project.create({
                                'name': data['name'],
                                'trello_project_id': data['id'],
                                'active': False if data['closed'] == True else True,
                            })
                        else:
                            existing_project.update({
                                'name': data['name'],
                                'trello_project_id': data['id'],
                                'active': False if data['closed'] == True else True,
                            })
        return project_data

    def get_trello_stages(self, user=None):
        stage = self.env['project.task.type']
        project_data = self.get_trello_projects(user)
        if user or self.env.user:
            trello_username = user.trello_username if user and user.trello_username else self.env.user.trello_username
            trello_api_key = user.trello_api_key if user and user.trello_api_key else self.env.user.trello_api_key
            trello_api_token = user.trello_api_token if user and user.trello_api_token else self.env.user.trello_api_token
            if trello_api_token and trello_api_key:
                for project_id in project_data:
                    url = "https://api.trello.com/1/boards/" + project_id + "/lists"
                    querystring = {"key": trello_api_key, "token": trello_api_token}
                    response = requests.request("GET", url, params=querystring)
                    if response:
                        datas = json.loads(response.text)
                        project_list = []
                        for data in datas:
                            if data['name'] in project_data[project_id]:
                                projects = self.env['project.project'].search(
                                    [('trello_project_id', '=', project_id)])
                                if projects.id:
                                    project_list.append(projects.id)
                                existing_stages = stage.search([('trello_stage_id', '=', data['id'])])
                                if not existing_stages:
                                    stage.create({
                                        'name': data['name'],
                                        'trello_stage_id': data['id'],
                                        'project_ids': [(6, 0, project_list)],
                                    })
                                else:
                                    existing_stages.update({
                                        'name': data['name'],
                                        'trello_stage_id': data['id'],
                                        'project_ids': [(6, 0, project_list)],
                                    })

    def get_trello_cards(self, user=None):
        tags = self.env['project.tags']
        task = self.env['project.task']
        if user or self.env.user:
            trello_username = user.trello_username if user and user.trello_username else self.env.user.trello_username
            trello_api_key = user.trello_api_key if user and user.trello_api_key else self.env.user.trello_api_key
            trello_api_token = user.trello_api_token if user and user.trello_api_token else self.env.user.trello_api_token
            project_data = self.get_trello_projects(user)
            if trello_api_key and trello_api_token:
                for project_id in project_data:
                    task_url = "https://api.trello.com/1/boards/" + project_id + "/cards"
                    task_querystring = {"key": trello_api_key, "token": trello_api_token}
                    task_response = requests.request("GET", task_url, params=task_querystring)
                    if task_response:
                        task_datas = json.loads(task_response.text)
                        for data in task_datas:
                            stage_id = self.env['project.task.type'].search([('trello_stage_id', '=', data['idList'])])
                            project_id = self.env['project.project'].search([('trello_project_id', '=', data['idBoard'])])
                            tag_list = []
                            for tag in data['labels']:
                                if tag['color'] == 'null':
                                    index = ''
                                elif tag['color'] == 'red':
                                    index = 1
                                elif tag['color'] == 'orange':
                                    index = 2
                                elif tag['color'] == 'yellow':
                                    index = 3
                                elif tag['color'] == 'light blue':
                                    index = 4
                                elif tag['color'] == 'dark purple':
                                    index = 5
                                elif tag['color'] == 'salmon pink':
                                    index = 6
                                elif tag['color'] == 'blue':
                                    index = 7
                                elif tag['color'] == 'dark blue':
                                    index = 8
                                elif tag['color'] == 'fushia':
                                    index = 9
                                elif tag['color'] == 'green':
                                    index = 10
                                elif tag['color'] == 'purple':
                                    index = 11
                                else:
                                    index = ''
                                existing_tags = tags.search([('name', '=', tag['name']),('project_id','=',project_id.id), ('color', '=', index)])
                                if not existing_tags:
                                    vals = {
                                        'name': tag['name'],
                                        'trello_tag_id': tag['id'],
                                        'color': index,
                                        'project_id': project_id.id,
                                    }
                                    tags.create(vals)
                                else:
                                    vals2 = {
                                        'name': tag['name'],
                                        'trello_tag_id': tag['id'],
                                        'color': index,
                                        'project_id': project_id.id
                                    }
                                    existing_tags.update(vals2)
                                tag_id = tags.search([('trello_tag_id', '=', tag['id'])])
                                for tag in tag_id:
                                    tag_list.append(tag.id)

                            existing_tasks = task.search([('trello_task_id', '=', data['id'])])
                            if not existing_tasks:
                                new_task = task.create({
                                    'name': data['name'],
                                    'sequence': data['pos'],
                                    'trello_task_id': data['id'],
                                    'project_id': project_id.id,
                                    'stage_id': stage_id.id,
                                    'tag_ids': [(6, 0, tag_list)],
                                    'date_deadline': data['due'],
                                    'description': data['desc'],
                                })
                                res_id = new_task.id
                            else:
                                existing_tasks.update({
                                    'name': data['name'],
                                    'sequence': data['pos'],
                                    'trello_task_id': data['id'],
                                    'project_id': project_id.id,
                                    'stage_id': stage_id.id,
                                    'tag_ids': [(6, 0, tag_list)],
                                    'date_deadline': data['due'],
                                    'description': data['desc'],
                                })
                                res_id = existing_tasks.id
                            attachment_url = "https://api.trello.com/1/cards/" + data['id'] + "/attachments"
                            attachment_querystring = {"key": trello_api_key, "token": trello_api_token}
                            attachment_response = requests.request("GET", attachment_url, params=attachment_querystring)
                            if attachment_response:
                                attachment_datas = json.loads(attachment_response.text)
                                for attachment in attachment_datas:
                                    attachment_id = self.env['ir.attachment'].search(
                                        [('trello_attachment_id', '=', attachment['id'])])
                                    if not attachment_id:
                                        self.env['ir.attachment'].create({
                                            'name': attachment['name'],
                                            'type': 'url',
                                            'url': attachment['url'],
                                            'res_model': 'project.task',
                                            'res_id': res_id,
                                            'trello_attachment_id': attachment['id'],
                                        })
                self.archive_datas(user)

    def sync_datas_to_trello(self, user=None):
        if user or self.env.user:
            trello_api_key = user.trello_api_key if user and user.trello_api_key else self.env.user.trello_api_key
            trello_api_token = user.trello_api_token if user and user.trello_api_token else self.env.user.trello_api_token
            projects = self.env['project.project'].search([])
            if trello_api_key and trello_api_token:
                for project in projects:
                    if project.trello_project_id:
                        project_url = "https://api.trello.com/1/boards/" + project.trello_project_id
                        project_querystring = {"key": trello_api_key, "token": trello_api_token,
                                               "closed": "true" if project.active == False else "false"}
                        project_response = requests.request("PUT", project_url, params=project_querystring)
                        if project_response:
                            project_response_datas = json.loads(project_response.text)
                            project.last_sync_at = fields.Datetime.now()
                        for stages in project.type_ids:
                            if stages.trello_stage_id:
                                stage_url = "https://api.trello.com/1/lists/" + stages.trello_stage_id
                                stage_querystring = {"name": stages.name, "idBoard": project.trello_project_id,
                                                     "pos": "bottom",
                                                     "key": trello_api_key, "token": trello_api_token}
                                stage_response = requests.request("PUT", stage_url, params=stage_querystring)
                            else:
                                stage_url = "https://api.trello.com/1/lists"
                                stage_querystring = {"name": stages.name, "idBoard": project.trello_project_id,
                                                     "pos": "bottom",
                                                     "key": trello_api_key, "token": trello_api_token}
                                stage_response = requests.request("POST", stage_url, params=stage_querystring)
                            if stage_response:
                                stage_response_datas = json.loads(stage_response.text)
                                stages.trello_stage_id = stage_response_datas['id']
                        for task in project.task_ids:
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
                                    tag_querystring = {"name": tag.name, "color": color, "key": trello_api_key,
                                                       "token": trello_api_token}
                                    tag_response = requests.request("PUT", tag_url, params=tag_querystring)
                                else:
                                    tag_url = "https://api.trello.com/1/labels"
                                    tag_querystring = {"name": tag.name, "color": color,
                                                       "idBoard": project.trello_project_id,
                                                       "key": trello_api_key, "token": trello_api_token}
                                    tag_response = requests.request("POST", tag_url, params=tag_querystring)
                                if tag_response:
                                    tag_response_datas = json.loads(tag_response.text)
                                    tag.trello_tag_id = tag_response_datas['id']
                                    label_list.append(tag.trello_tag_id)
                            if task.trello_task_id:
                                task_url = "https://api.trello.com/1/cards/" + task.trello_task_id
                                task_querystring = {"idList": task.stage_id.trello_stage_id, "name": task.name,
                                                    "pos": task.sequence,
                                                    "desc": TAG_RE.sub('',
                                                                       task.description) if task.description else '',
                                                    "due": task.date_deadline if task.date_deadline else '',
                                                    "keepFromSource": "all", "idLabels": label_list,
                                                    "closed": "true" if task.active == False else "false",
                                                    "key": trello_api_key, "token": trello_api_token}
                                task_response = requests.request("PUT", task_url, params=task_querystring)
                            else:
                                task_url = "https://api.trello.com/1/cards"
                                task_querystring = {"idList": task.stage_id.trello_stage_id, "name": task.name,
                                                    "pos": task.sequence,
                                                    "desc": TAG_RE.sub('',
                                                                       task.description) if task.description else '',
                                                    "due": task.date_deadline if task.date_deadline else '',
                                                    "keepFromSource": "all", "idLabels": label_list,
                                                    "closed": "true" if task.active == False else "false",
                                                    "key": trello_api_key, "token": trello_api_token}
                                task_response = requests.request("POST", task_url, params=task_querystring)
                            if task_response:
                                task_response_datas = json.loads(task_response.text)
                                task.trello_task_id = task_response_datas['id']
                            for attachment in task.attachment_ids:
                                if not attachment.trello_attachment_id:
                                    file_path = attachment._full_path(attachment.store_fname)
                                    attachment_url = "https://api.trello.com/1/cards/" + task.trello_task_id + "/attachments"
                                    attachment_querystring = {"key": trello_api_key, "token": trello_api_token,
                                                              "name": attachment.name}
                                    files = {'file': open(file_path, 'rb')}
                                    attachment_response = requests.request("POST", attachment_url,
                                                                           params=attachment_querystring,
                                                                           files=files)
                                    if attachment_response:
                                        attachment_datas = json.loads(attachment_response.text)
                                        attachment.trello_attachment_id = attachment_datas['id']
                            task.last_sync_at = fields.Datetime.now()
                    else:
                        project_url = "https://api.trello.com/1/boards/"
                        project_querystring = {"name": project.name, "defaultLists": "false", "key": trello_api_key,
                                               "token": trello_api_token,
                                               "closed": "true" if project.active == False else "false"}
                        project_response = requests.request("POST", project_url, params=project_querystring)
                        print("project_responsejjjjjjjjjjjjjj",project_response,project.name)
                        if project_response:
                            project_response_datas = json.loads(project_response.text)
                            project.trello_project_id = project_response_datas['id']
                            project.last_sync_at = fields.Datetime.now()
                        for stages in project.type_ids:
                            stage_url = "https://api.trello.com/1/boards/" + project.trello_project_id + "/lists"
                            stage_querystring = {"name": stages.name, "pos": "bottom", "key": trello_api_key,
                                                 "token": trello_api_token}
                            stage_response = requests.request("POST", stage_url, params=stage_querystring)
                            if stage_response:
                                stage_response_datas = json.loads(stage_response.text)
                                stages.trello_stage_id = stage_response_datas['id']
                        for task in project.task_ids:
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
                                    tag_querystring = {"name": tag.name, "color": color, "key": trello_api_key,
                                                       "token": trello_api_token}
                                    tag_response = requests.request("PUT", tag_url, params=tag_querystring)
                                else:
                                    tag_url = "https://api.trello.com/1/labels"
                                    tag_querystring = {"name": tag.name, "color": color,
                                                       "idBoard": project.trello_project_id,
                                                       "key": trello_api_key, "token": trello_api_token}
                                    tag_response = requests.request("POST", tag_url, params=tag_querystring)
                                if tag_response:
                                    tag_response_datas = json.loads(tag_response.text)
                                    tag.trello_tag_id = tag_response_datas['id']
                                    label_list.append(tag.trello_tag_id)
                            if task.trello_task_id:
                                task_url = "https://api.trello.com/1/cards/" + task.trello_task_id
                                task_querystring = {"idList": task.stage_id.trello_stage_id, "name": task.name,
                                                    "pos": task.sequence,
                                                    "desc": TAG_RE.sub('',
                                                                       task.description) if task.description else '',
                                                    "due": task.date_deadline if task.date_deadline else '',
                                                    "keepFromSource": "all", "idLabels": label_list,
                                                    "closed": "true" if task.active == False else "false",
                                                    "key": trello_api_key, "token": trello_api_token}
                                task_response = requests.request("PUT", task_url, params=task_querystring)
                            else:
                                task_url = "https://api.trello.com/1/cards"
                                task_querystring = {"idList": task.stage_id.trello_stage_id, "name": task.name,
                                                    "pos": task.sequence,
                                                    "desc": TAG_RE.sub('',
                                                                       task.description) if task.description else '',
                                                    "due": task.date_deadline if task.date_deadline else '',
                                                    "keepFromSource": "all", "idLabels": label_list,
                                                    "closed": "true" if task.active == False else "false",
                                                    "key": trello_api_key, "token": trello_api_token}
                                task_response = requests.request("POST", task_url, params=task_querystring)
                            if task_response:
                                task_response_datas = json.loads(task_response.text)
                                task.trello_task_id = task_response_datas['id']
                            for attachment in task.attachment_ids:
                                if not attachment.trello_attachment_id:
                                    file_path = attachment._full_path(attachment.store_fname)
                                    attachment_url = "https://api.trello.com/1/cards/" + task.trello_task_id + "/attachments"
                                    attachment_querystring = {"key": trello_api_key, "token": trello_api_token,
                                                              "name": attachment.name}
                                    files = {'file': open(file_path, 'rb')}
                                    attachment_response = requests.request("POST", attachment_url,
                                                                           params=attachment_querystring,
                                                                           files=files)
                                    if attachment_response:
                                        attachment_datas = json.loads(attachment_response.text)
                                        attachment.trello_attachment_id = attachment_datas['id']
                            task.last_sync_at = fields.Datetime.now()

    def archive_datas(self,user=None):
        tasks = self.env['project.task'].search([])
        stages = self.env['project.task.type'].search([])
        attachments = self.env['ir.attachment'].search([])
        if user or self.env.user:
            trello_api_key = user.trello_api_key if user and user.trello_api_key else self.env.user.trello_api_key
            trello_api_token = user.trello_api_token if user and user.trello_api_token else self.env.user.trello_api_token
            if trello_api_key and trello_api_token:
                project_data = self.get_trello_projects(user)
                trello_card_ids = []
                trello_stage_ids = []
                trello_attachment_ids = []
                for project_id in project_data:
                    task_url = "https://api.trello.com/1/boards/" + project_id + "/cards"
                    task_querystring = {"key": trello_api_key, "token": trello_api_token}
                    task_response = requests.request("GET", task_url, params=task_querystring)
                    if task_response:
                        task_datas = json.loads(task_response.text)
                    stage_url = "https://api.trello.com/1/boards/" + project_id + "/lists"
                    stage_querystring = {"key": trello_api_key, "token": trello_api_token}
                    stage_response = requests.request("GET", stage_url, params=stage_querystring)
                    if stage_response:
                        stage_datas = json.loads(stage_response.text)
                        for stage_data in stage_datas:
                            trello_stage_ids.append(stage_data['id'])
                    if task_datas:
                        for task_data in task_datas:
                            trello_card_ids.append(task_data['id'])
                            attachment_url = "https://api.trello.com/1/cards/" + task_data['id'] + "/attachments"
                            attachment_querystring = {"key": trello_api_key, "token": trello_api_token}
                            attachment_response = requests.request("GET", attachment_url, params=attachment_querystring)
                            if attachment_response:
                                attachment_datas = json.loads(attachment_response.text)
                                for attachment_data in attachment_datas:
                                    trello_attachment_ids.append(attachment_data['id'])
                for task in tasks:
                    if task.trello_task_id not in trello_card_ids:
                        existing_task = self.env['project.task'].search(
                            [('trello_task_id', '=', task.trello_task_id), ('trello_task_id', '!=', False)])
                        if existing_task:
                            existing_task.active = False
                for stage in stages:
                    if stage.trello_stage_id not in trello_stage_ids:
                        existing_stage = self.env['project.task.type'].search(
                            [('trello_stage_id', '=', stage.trello_stage_id), ('trello_stage_id', '!=', False)])
                        if existing_stage:
                            existing_stage.unlink()
                for attachment in attachments:
                    if attachment.trello_attachment_id not in trello_attachment_ids:
                        existing_attachment = self.env['ir.attachment'].search(
                            [('trello_attachment_id', '=', attachment.trello_attachment_id),
                             ('trello_attachment_id', '!=', False)])
                        if existing_attachment:
                            existing_attachment.unlink()
