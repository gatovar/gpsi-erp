# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class CertificationContract(models.Model):
	'''
	Model para la aplicación de certificado.
	'''

	_name = 'gpsi.sale.contract'
	_description = 'Contract Certification'
	_inherit = 'mail.thread'

	standard = fields.Char('Standard')#
	client = fields.Char('Client')#
	representative = fields.Char('Representative')#
	representative_position = fields.Char('Representative Position')#
	events = fields.Char('Events')##
	notes = fields.Text('Notes')
	conditions = fields.Text('Special Conditions')
	date_contract = fields.Date('Date')

	sqf_scope = fields.Text('Scope')#
	sqf_code = fields.Char('Code')#
	sqf_level = fields.Char('Level')#
	sqf_adress = fields.Text('Adress')#
	sqf_phone = fields.Char('Phone')#
	sqf_date = fields.Date('Date Audit')
	