# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hospital.patient'
    _rec_name = 'patient_name'

    patient_name = fields.Char(string='name')
    patient_age = fields.Integer('age')
    note = fields.Text('note')
  
