# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Users(models.Model):
    _inherit = 'res.users'

    @api.multi
    def is_anonymous(self):
        self.ensure_one()
        return self.login == 'anonymous'
        