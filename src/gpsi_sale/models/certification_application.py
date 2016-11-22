# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CertificactionApplication(models.Model):
    """
    Model para la aplicación de certificado.
    """
    _name = 'gpsi.sale.application.certification'
    _description = 'Application Certification'
