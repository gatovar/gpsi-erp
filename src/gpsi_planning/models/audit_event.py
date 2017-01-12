# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class AuditEventAuditor(models.Model):
    _name = 'gpsi.planning.audit.event.auditor'
    _description = 'Auditor'

    audit_id = fields.Many2one('gpsi.planning.audit.event', 'Event')
    user_id = fields.Many2one('res.users', 'User')
    is_leader = fields.Boolean('Leader')¡


class AuditEvent(models.Model):
    _name = 'gpsi.planning.audit.event'
    _inherit = ['mail.thread']

    event_type = fields.Selection([('preaudit', 'Pre-Audit'), ('stage1', 'Stage I'), ('stage2', 'Stage 2')], 'Event Type')
    standard_id = fields.Many2one('gpsi.sale.contract.standard', 'Standard')
    auditor_ids = fields.One2many('gpsi.planning.audit.event.auditor', 'audit_id', 'Auditors')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    notes = fields.Text('Notes')
    review_notes = fields.Text('Review Notes')
