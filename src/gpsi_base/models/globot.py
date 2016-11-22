# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Globot(models.Model):
    _inherit = 'res.users'

    @api.model
    def find_globot(self):
        return self.env['res.users'].search([('login','=','globot@globalstd.com')])
