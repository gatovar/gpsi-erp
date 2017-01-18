# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    gs_tag_ids = fields.Many2many('gpsi.project.tags', string='Tags')


class Tag(models.Model):
    _name = "gpsi.project.tag"
    _description = "Project Category"

    name = fields.Char("Tag", required=True)
    color = fields.Integer('Color Index')
    gs_project_ids = fields.Many2many('project.project', string='Projects')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]