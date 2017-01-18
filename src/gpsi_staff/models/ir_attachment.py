# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

class Attachments(models.Model):
    _inherit = 'ir.attachment'

    gs_tag_ids = fields.Many2many('ir.attachment.category', string='Attachment Category')

class AttachmentCategory(models.Model):
    _name = "ir.attachment.category"
    _description = "Attachment Category"

    name = fields.Char("Attachment Tag", required=True)
    color = fields.Integer('Color Index')
    gs_tag_ids = fields.Many2many('ir.attachment', string='Attachment')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]