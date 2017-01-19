# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class EmployeeProfile(models.Model):
    _name = 'hr.employee.profile'
    _description = 'Employee Profile'
