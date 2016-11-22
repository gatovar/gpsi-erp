# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Task(models.Model):
    _inherit = 'project.task'

    bpm_assignee = fields.Many2one('res.users', 'Assignee')
    bpm_canditate_user_ids = fields.One2many('res.users', 'bpm_task_id', 'Users')
    bpm_canditate_group_ids = fields.One2many('res.groups', 'bpm_task_id', 'Users')

