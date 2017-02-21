# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Certificate(models.Model):
    _name = 'gpsi.sale.certificate'
    _description = 'Certificate'
    