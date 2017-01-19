# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

class Course(models.Model):
    _inherit = 'event.event'

    gs_instructor_id = fields.Many2one('res.users', 'Instructor')