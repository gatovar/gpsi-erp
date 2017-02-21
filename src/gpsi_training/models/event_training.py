# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Event(models.Model):
    _inherit = 'event.event'

    gs_type = fields.Selection(
        string='Type',
        selection=[('requirements', 'Requirements'), ('internal', 'Internal Auditor'), ('leader', 'Leader Auditor')]
    )
    gs_body_id = fields.Many2one(
        string='Body',
        comodel_name='event.event.body'
    )
    gs_compentecy_ids = fields.Many2many(
        string='Competencies',
        comodel_name='event.event.body.competency'
    )
    

class Attendee(models.Model):
    _inherit = 'event.registration'

    gs_date_exam = fields.Date('Competency examination date')
    gs_date_cert = fields.Date('Certificate date of issue')
    gs_cert_number = fields.Char('Certificate number')

class Body(models.Model):
    _name = "event.event.body"

    name = fields.Char("Name")
    competency_ids = fields.One2many(
        string='Competencies',
        comodel_name='event.event.body.competency',
        inverse_name='body_id'
    )

class Competency(models.Model):
    _name = "event.event.body.competency"

    name = fields.Char("Name")
    code = fields.Char("Code")
    body_id = fields.Many2one(
        string='Training Body',
        comodel_name='event.event.body'
    )
