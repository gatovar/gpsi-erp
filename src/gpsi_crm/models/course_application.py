# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CourseApplication(models.Model):
    """
    Modelo para la aplicación de un curso.
    """
    _name = 'gpsi.sale.application.course'
    _description = 'Application Course'
