# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Transaction(models.Model):
    _name = 'transaction.transaction'
    _description = 'Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    STATUS_SELECTION = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]


    partner_id = fields.Many2one('res.partner',"Citizen", required=True)
    date = fields.Date("Date", default=fields.Date.today)
    national_num = fields.Char(string='National ID',related='partner_id.national_number', readonly=False, required=True)
    reference_no = fields.Char(string='Order Reference', required=True,readonly=True, default=lambda self:('New'))
    transaction_line_ids = fields.One2many(comodel_name='transaction.line',inverse_name='transaction_id')
    tr_type_id = fields.Many2one('transaction.type', string='Transaction Type', required=True)
    total_amount= fields.Float(string='Total Amount',readonly=True)
    fee_type = fields.Selection([('fixed', 'Fixed'), ('chengable', 'Changable')], string='Fees Type', required=True)
    message_ids = fields.One2many('mail.message', 'res_id', domain=[('model', '=', 'transaction.transaction')],
                                  string='Messages', copy=False)
    status = fields.Selection(selection=STATUS_SELECTION, string='Status', default='draft')


    def total_amount_create_invoice (self):
        total= 0.0
        for record in self.transaction_line_ids:
            
            print(record.tr_type_id.transaction_amount,"###")
            total += float(record.tr_type_id.transaction_amount)
            print(total)
            self.total_amount = total
            invoice_model = self.env['account.move']

            invoice_vals = {
                'partner_id': self.partner_id.id,
                'invoice_date': self.date,
                'invoice_line_ids': [
                    (0, 0, {
                        'name':record.tr_type_id.name,
                        'quantity': 1,
                        'price_unit': record.tr_type_id.transaction_amount,
                        'account_id': self.partner_id.property_account_receivable_id.id,
                    }),
                ],
            }

            new_invoice = invoice_model.create(invoice_vals)

        # Open the created invoice form view
            return {
                'name': 'Invoice Created',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': new_invoice.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
            }
        
    def confirm_transaction(self):
        unpaid_invoices = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid'),
        ])

        print("Unpaid Invoices:", unpaid_invoices)

        if unpaid_invoices:
            raise ValueError("Cannot confirm the transaction. There are unpaid invoices.")
        
        print("Transaction confirmed successfully.")
        self.write({'status': 'confirmed'})

    def cancel_transaction(self):
        self.write({'status': 'cancelled'})


class Citizen(models.Model):
    _inherit = 'res.partner'
    _description = 'Citizens'

    national_number = fields.Char(string='National ID', required=True, unique=True)
    

class TransactionType(models.Model):
    _name = 'transaction.type'
    _description = 'Transaction Types'

    name = fields.Char(string='Transaction Type', required=True)
    transaction_amount = fields.Float(string = "Transaction Fee")


class TransactionFee(models.Model):
    _name = 'transaction.fee'
    _description = 'Transaction Fees'

    name = fields.Char(string='Fee Name', required=True)
    amount = fields.Float(string='Amount')



class TransactionLine(models.Model):
    _name = 'transaction.line'

    tr_type_id = fields.Many2one('transaction.type', string='Transaction Type', required=True)
    tr_fee = fields.Char(string = "Transaction Fee")
    transaction_id = fields.Many2one('transaction.transaction')

