# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    gs_gaudit_company_id = fields.Many2one('res.company', 'Related Company')
