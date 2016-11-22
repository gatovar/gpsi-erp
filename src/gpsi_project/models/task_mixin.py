# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class TaskResourceAttachment(models.Model):
    _name = 'gpsi.task.resource.attachment'
    _description = 'Resource Attachment'
    _order = 'id desc'

    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade')
    res_name = fields.Char('Resource Name', compute='_compute_res_name', store=True)
    res_model = fields.Char('Resource Model', required=True, help="The database object this attachment will be attached to.")
    res_id = fields.Integer('Resource ID', required=True, help="The record id this is attached to.")

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for attachment in self:
            if attachment.res_model and attachment.res_id:
                record = self.env[attachment.res_model].browse(attachment.res_id)
                attachment.res_name = record.display_name


class Task(models.Model):
    _inherit = 'project.task'

    res_attachment_ids = fields.One2many('gpsi.task.resource.attachment', 'task_id', 'Resource Attachments')

    def get_current_res_attachment(self):
        self.ensure_one()
        pass


class TaskMixin(models.Model):
    _name = 'gpsi.project.task.mixin'
    _description = 'Task Mixin'

    task_id = fields.Many2one('project.task', 'Task', compute='_compute_task_id')
    task_name = fields.Char(related='task_id.name')
    task_description = fields.Html(related='task_id.description')
    task_kanban_state = fields.Selection(related='task_id.kanban_state')
    task_priority = fields.Selection(related='task_id.priority')

    def _compute_task_id(self):
        attach_model = self.env['gpsi.task.resource.attachment']
        for record in self:
            attachment = attach_model.search([('res_model','=',record._name), ('res_id','=',record.id)])
            record.task_id = attachment and attachment.task_id or False
