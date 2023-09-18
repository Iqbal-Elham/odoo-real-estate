# -*- coding: utf-8 -*-
# from odoo import http


# class BankingSystem(http.Controller):
#     @http.route('/banking_system/banking_system', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/banking_system/banking_system/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('banking_system.listing', {
#             'root': '/banking_system/banking_system',
#             'objects': http.request.env['banking_system.banking_system'].search([]),
#         })

#     @http.route('/banking_system/banking_system/objects/<model("banking_system.banking_system"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('banking_system.object', {
#             'object': obj
#         })
