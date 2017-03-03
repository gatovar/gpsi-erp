# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Supplier(models.Model):
    _inherit = 'res.partner'

    def create(self, vals):
        pass

    def _aii_create_supplier(self):
        pass

    def _aii_find_supplier(self):
        pass