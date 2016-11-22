# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    bpm_project_id = fields.Many2one('project.project', 'Project')
