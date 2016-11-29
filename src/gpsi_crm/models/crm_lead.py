# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead']

    gpsi_opportunity_type = fields.Selection(
        selection=[
            ('course', 'Course'),
            ('certification_audit', 'Certification Audit'),
            ('vendor_audit', 'Vendor Audit')],
        string='Type', default='course')
    gpsi_cert_app = fields.Many2one('gpsi.crm.application.certification', 'Certification Application')        
