# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.models import BaseModel
from odoo.exceptions import UserError, ValidationError

from lxml import etree

def fields_view_get_decorator(method):
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result =  method(self, view_id, view_type, toolbar, submenu)
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            node = doc.xpath("//form")[0]
            node.set('edit', 'false')
            node.set('create', 'false')
            result['arch'] = etree.tostring(doc)
        return result

    return fields_view_get

BaseModel.fields_view_get = fields_view_get_decorator(BaseModel.fields_view_get)

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
            'gs_res_ids': [(0, 0, {'task_id': self.id, 'res_model': record._name,'res_id': record.id})]
        })

    @api.multi
    def gs_del_res(self, record):
        self.ensure_one()
        res = self.gs_res_ids.filtered(lambda r: r.res_model == record._name and r.res_id == record.id)
        self.write({
            'gs_res_ids': [(2, res.id, False)]
        })
        

class BpmTaskResource(models.Model):
    _name = 'gpsi.bpm.task.resource'
    _description = 'Task Resource'
    _order = 'id desc'

    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade')
    res_name = fields.Char('Name', compute='_compute_res_name')
    res_desc = fields.Char('Description', compute='_compute_res_desc')
    res_model = fields.Char('Model', required=True, help="The database object this attachment will be attached to.")
    res_id = fields.Integer('ID', required=True, help="The record id this is attached to.")
    view_id = fields.Char('View ID')
    perm_write = fields.Boolean('Write Access', default=True)
    perm_create = fields.Boolean('Create Access', default=True)
    perm_delete = fields.Boolean('Delete Access', default=True)

    @api.model
    def create(self, vals):
        res = super(BpmTaskResource, self).create(vals)
        if res.res_model and res.res_id:
            rec = self.env[res.res_model].search([('id','=',res.res_id)])
            if rec:
                rec.write({'task_ids': [(4, res.task_id.id, False)]})
        return rec

    @api.multi
    def unlink(self):
        for res in self:
            if res.res_model and res.res_id:
                rec = self.env[rec.res_model].search([('id','=',res.res_id)])
                if rec:
                    rec.write({'task_ids': [(3, res.task_id.id, False)]})
        return super(BpmTaskResource, self).unlink()

    @api.depends('res_model', 'res_id')
    def _compute_res_name(self):
        for res in self:
            if res.res_model and res.res_id:
                record = self.env[res.res_model].browse(res.res_id)
                res.res_name = record.display_name

    @api.depends('res_model')
    def _compute_res_desc(self):
        for res in self:
            if res.res_model:
                record = self.env['ir.model'].search([('model','=',res.res_model)])
                res.res_desc = record.name

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
        

class BpmTaskMixin(models.AbstractModel):
    _name = 'gpsi.bpm.task.mixin'

    task_ids = fields.Many2many('project.task', 'Tasks')


class ResUser(models.Model):
    _inherit = 'res.users'

    gs_assigned_task_ids = fields.One2many('project.task', 'user_id', 'Assigned Tasks')
