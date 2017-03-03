# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Company(models.Model):
    _inherit = 'res.company'

    gs_customer_audit_ids = fields.Many2many('project.task', 'gpsi_staff_company_customer_audit_rel', 'company_id', 'audit_id', 'Customer Audits')
