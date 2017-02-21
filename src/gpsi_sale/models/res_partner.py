# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class ResPartner(models.Models):
    _inherit = 'res.partner'
