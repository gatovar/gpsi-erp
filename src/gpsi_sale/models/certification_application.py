# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CertificactionApplication(models.Model):
    _name = 'gpsi.sale.application.certification'
    