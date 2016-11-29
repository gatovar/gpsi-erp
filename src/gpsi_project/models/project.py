# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    bpm_assignee_id = fields.Many2one('res.users', 'Assignee')
    bpm_canditate_ids = fields.Many2many('res.users', string='Candidate Users')
    bpm_canditate_group_ids = fields.Many2many('res.groups', string='Candidate Groups')
