# -*- coding: utf-8 -*-
# from odoo import http


# class ProductTest(http.Controller):
#     @http.route('/product_test/product_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_test/product_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_test.listing', {
#             'root': '/product_test/product_test',
#             'objects': http.request.env['product_test.product_test'].search([]),
#         })

#     @http.route('/product_test/product_test/objects/<model("product_test.product_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_test.object', {
#             'object': obj
#         })
