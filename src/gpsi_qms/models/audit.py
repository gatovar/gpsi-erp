# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AuditOrder(models.Model):
    _name = 'gpsi.qms.audit.order'
    _description = 'Audit Order'
