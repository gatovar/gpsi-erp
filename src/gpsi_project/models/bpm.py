# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    gs_assignee_id = fields.Many2one('res.users', 'Assignee')
    gs_canditate_ids = fields.Many2many('res.users', string='Candidate Users')
    gs_canditate_group_ids = fields.Many2many('res.groups', string='Candidate Groups') 


class ProjectTask(models.Model):
    _inherit = 'project.task'

    gs_claim_visible = fields.Boolean('Claim Visible', compute='_compute_gs_claim_visible')
    gs_res_ids = fields.One2many('gpsi.bpm.task.resource', 'task_id', 'Resources')

    @api.depends()
    def _compute_gs_claim_visible(self):
        for task in self:
            task.gs_claim_visible = task.user_id == False and task.stage_id.gs_canditate_ids in [self.env.user]

    @api.multi
    def action_claim(self):
        self.ensure_one()
        self.write({
            'user_id': self.env.user.id
        })

    @api.multi
    def gs_add_res(self, record):
        self.ensure_one()
        self.write({
            'gs_res_ids': [(0, 0, {
                'task_id': self.id,
                'res_model': record._name,
                'res_id': record.id
            })]
        })
        

class TaskResourceAttachment(models.Model):
    _name = 'gpsi.bpm.task.resource'
    _description = 'Resource Attachment'
    _order = 'id desc'

    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade')
    res_name = fields.Char('Resource Name', compute='_compute_res_name')
    res_model = fields.Char('Resource Model', required=True, help="The database object this attachment will be attached to.")
    res_id = fields.Integer('Resource ID', required=True, help="The record id this is attached to.")
    view_id = fields.Char('View ID')

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for attachment in self:
            if attachment.res_model and attachment.res_id:
                record = self.env[attachment.res_model].browse(attachment.res_id)
                attachment.res_name = record.display_name

    @api.multi
    def action_open_resource(self):
        self.ensure_one()
        action = {
            'name': 'Open Resource',
            'view_mode': 'form',
            'res_model': self.res_model,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': self.res_id
        }
        if self.view_id:
            action['view_id'] = self.env.ref(self.view_id).id
        return action                               
        

class ProjectTaskMixin(models.AbstractModel):
    _name = 'gpsi.bpm.task.mixin'

    task_id = fields.Many2one('project.task', 'Task', compute='_compute_task_id')
    task_name = fields.Char(related='task_id.name')
    task_description = fields.Html(related='task_id.description')
    task_kanban_state = fields.Selection(related='task_id.kanban_state')
    task_priority = fields.Selection(related='task_id.priority')

    def _compute_task_id(self):
        attach_model = self.env['gpsi.bpm.task.resource']
        for record in self:
            attachment = attach_model.search([('res_model','=',record._name), ('res_id','=',record.id)])
            record.task_id = attachment and attachment.task_id or False
        