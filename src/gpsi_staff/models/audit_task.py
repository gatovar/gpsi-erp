# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for i in xrange(20))


class AuditProject(models.Model):
    _inherit = 'project.project'

    gs_is_cert_audit = fields.Boolean('Cert. Audit', help='Mark task like certification audit')
    gs_is_vendor_audit = fields.Boolean('Vendor Audit', help='Mark project like vendor audit')

    @api.model
    def create(self, vals):
        res = super(AuditProject, self).create(vals)
        res._gs_init_stages()
        return res

    def _gs_init_stages(self):
        if not self.gs_is_vendor_audit:
            return

        self.env.ref('gpsi_staff.vendor_audit_new_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_scheduling_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_execute_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_review_stage').write({'project_ids': [(4, self.id, False)]})
        self.env.ref('gpsi_staff.vendor_audit_closed_stage').write({'project_ids': [(4, self.id, False)]})


class AuditTask(models.Model):
    _inherit = 'project.task'

    gs_checklist_id = fields.Many2one('gpsi.staff.checklist', 'Checklist', domain=[('is_template','=',True)])
    gs_assessment_id = fields.Many2one('gpsi.staff.checklist', 'Assessment')
    gs_audit_team_ids = fields.One2many('gpsi.staff.audit.team.member', 'task_id', 'Team')
    gs_car_ids = fields.One2many('gpsi.staff.audit.car', 'audit_id', 'Action Requests')
    gs_car_count = fields.Integer('CAR Count', compute='_gs_compute_car_count')
    
    @api.model
    def create(self, vals):
        res = super(AuditTask, self).create(vals)
        res._gs_create_assessment()
        res._gs_send_invitation()
        return res

    def _gs_create_assessment(self):
        if not self.project_id and not self.project_id.gs_is_vendor_audit:
            return

        assessment = self.gs_checklist_id.create_assessment()
        self.write({
            'gs_assessment_id': assessment.id
        })

    def _gs_send_invitation(self):
        if self.partner_id.gs_gaudit_company_id:
            self.partner_id.gs_gaudit_company_id.write({
                'gs_customer_audit_ids': [(4, self.id, False)]
            })
            return

    @api.multi
    def _gs_compute_car_count(self):
        for rec in self:
            rec.gs_car_count = len(rec.gs_car_ids)
        
    @api.multi
    def action_gs_edit_assessment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/ga/admin/va/events/{0}/assessment/edit'.format(self.id),
            'target': 'new'
        }

    @api.multi
    def action_gs_open_cars(self):
        self.ensure_one()
        return {
            "type": 'ir.actions.act_window',
            "res_model": 'gpsi.staff.audit.car',
            "views": [[False, 'tree'], [False, 'form']],
            "domain": [('audit_id', '=', self.id)],
            "context": {'default_audit_id': self.id},
            "name": "Corrective Action Requests",
        }
        

class AuditMember(models.Model):
    _name = 'gpsi.staff.audit.team.member'
    _description = 'Audit Member'

    task_id = fields.Many2one('project.task', 'Audit Task')
    user_id = fields.Many2one('res.users', 'User')
    role = fields.Selection([('lead', 'Lead'), ('observer', 'Observer'), ('witness', 'Witness')], 'Role')


class CAR(models.Model):
    _name = 'gpsi.staff.audit.car'
    _description = 'CAR'
    _inherit = ['mail.thread']

    audit_id = fields.Many2one('project.task', 'Audit')
    active = fields.Boolean('Active', default=True)
    due_date = fields.Date('Due Date')
    nonconformity = fields.Html('Nonconformity')
    correction = fields.Html('Inmediate Correction')
    root_cause = fields.Html('Root Cause Analysis')
    action_plan = fields.Html('Action Plans')
    conclusion = fields.Html('Conclusion')
    state = fields.Selection([('open','Open'), ('review','Review'), ('closed', 'Closed'), ('cancelled', 'Cancelled')], 'State', default='open')
