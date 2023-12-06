# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Product_Test(models.Model):
   _inherit = 'product.template'

   name_alter = fields.Char(string="Name")
   alter_ids = fields.Many2many("product.product", "product_tmpl", string="Alternative Products")


class Purchase_Test(models.Model):
   _inherit = 'purchase.order'
   
   prodct_alternaitve_ids = fields.Many2many("product.product", string="Product Alternaitve")   
   base_product = fields.Char(string="Original Product")
   onhand_qty = fields.Float(compute='_compute_onhand_qty', string='On Hand Quantity')
   forecast_qty = fields.Float(compute='_compute_forecast_qty', string='Forecast Quantity')

   @api.onchange('order_line')
   def onchange_alter_ids(self):
      for rec in self:
         alternative_ids = []
         base_product = False
         onhand_qty = 0
         forecast_qty = 0
         
         for order_line in rec.order_line:
               if order_line.product_id:
                  alternative_products = order_line.product_id.alter_ids
                  alternative_ids += [i.id for i in alternative_products]
                  base_product = order_line.product_id.name_alter
                  onhand_qty = order_line.product_id.virtual_available
                  forecast_qty = order_line.product_id.virtual_available

         rec.write({
               'prodct_alternaitve_ids': [(6, 0, alternative_ids)],
               'base_product': base_product,
               'onhand_qty': onhand_qty,
               'forecast_qty': forecast_qty,
         })

