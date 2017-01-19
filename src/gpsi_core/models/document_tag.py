# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    gs_tag_ids = fields.Many2many('ir.attachment.tag', string='Tags')


class Tag(models.Model):
    _name = "ir.attachment.tag"
    _description = "Attachment Category"

    name = fields.Char("Tag", required=True)
    color = fields.Integer('Color Index')
    gs_attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    