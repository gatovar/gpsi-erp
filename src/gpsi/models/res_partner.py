# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    