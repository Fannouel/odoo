# -*- coding: utf-8 -*-
# from odoo import http


# class Reportfig(http.Controller):
#     @http.route('/reportfig/reportfig', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reportfig/reportfig/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reportfig.listing', {
#             'root': '/reportfig/reportfig',
#             'objects': http.request.env['reportfig.reportfig'].search([]),
#         })

#     @http.route('/reportfig/reportfig/objects/<model("reportfig.reportfig"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reportfig.object', {
#             'object': obj
#         })
