# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Attendee(models.Model):
    _inherit = 'event.registration'

    gs_certificate_delivery_policy = fields.Selection([('me','Me'), ('company','Company'), ('both','Both')], default="me", string='Certificate Delivery Policy')
