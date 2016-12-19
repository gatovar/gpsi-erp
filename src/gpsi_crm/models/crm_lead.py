# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead', 'gpsi.bpm.task.mixin']
