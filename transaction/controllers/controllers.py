# -*- coding: utf-8 -*-
# from odoo import http


# class Transaction(http.Controller):
#     @http.route('/transaction/transaction', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transaction/transaction/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('transaction.listing', {
#             'root': '/transaction/transaction',
#             'objects': http.request.env['transaction.transaction'].search([]),
#         })

#     @http.route('/transaction/transaction/objects/<model("transaction.transaction"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transaction.object', {
#             'object': obj
#         })
