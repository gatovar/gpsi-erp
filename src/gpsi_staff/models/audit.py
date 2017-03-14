# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

FIELD_TYPES = [
    ('boolean', 'Boolean'), 
    ('char', 'Char'), 
    ('int', 'Integer'), 
    ('float', 'Float'), 
    ('date', 'Date'), 
    ('text', 'Text'), 
    ('html', 'Html')]

CAR_STAGES = [
    ('open','Open'), 
    ('review','Review'), 
    ('closed', 'Closed')]
    

class AuditProject(models.Model):
    _inherit = 'project.project'

    is_cert_audit = fields.Boolean('Cert. Audit', help='Mark task like certification audit')
    is_supplier_audit = fields.Boolean('Vendor Audit', help='Mark project like vendor audit')

    @api.model
    def create(self, vals):
        res = super(AuditProject, self).create(vals)
        res._init_audit_stages()
        return res

    def _init_audit_stages(self):
        if self.is_supplier_audit:
            self.env.ref('gpsi_staff.vendor_audit_new_stage').write({'project_ids': [(4, self.id, False)]})
            self.env.ref('gpsi_staff.vendor_audit_scheduling_stage').write({'project_ids': [(4, self.id, False)]})
            self.env.ref('gpsi_staff.vendor_audit_execute_stage').write({'project_ids': [(4, self.id, False)]})
            self.env.ref('gpsi_staff.vendor_audit_review_stage').write({'project_ids': [(4, self.id, False)]})
            self.env.ref('gpsi_staff.vendor_audit_closed_stage').write({'project_ids': [(4, self.id, False)]})


class AuditTask(models.Model):
    _inherit = 'project.task'

    audit_id = fields.Many2one('gpsi.staff.audit', 'Audit')
    is_cert_audit = fields.Boolean(related='project_id.is_cert_audit')
    is_supplier_audit = fields.Boolean(related='project_id.is_supplier_audit')

    @api.model
    def create(self, vals):
        task = super(AuditTask, self).create(vals)
        return task


class Audit(models.Model):
    """
    Auditoría
    """
    _name = 'gpsi.staff.audit'
    _description = 'Audit'
    _inherit = ['mail.thread']

    chk_id = fields.Many2one('gpsi.staff.audit.chk', 'Checklist', domain=[('is_template','=',True)], help='Checklist')
    asst_id = fields.Many2one('gpsi.staff.audit.chk', 'Assessment', domain=[('is_template','=',False)], help='Assessment')
    active = fields.Boolean('Active', default=True)
    execution_date = fields.Date('Date')
    auditee_id = fields.Many2one('res.partner', 'Auditee')
    auditor_id = fields.Many2one('res.partner', compute='_compute_auditor_id', help='Auditor lead')
    member_ids = fields.One2many('gpsi.staff.audit.member', 'audit_id', 'Audit Team')
    car_ids = fields.One2many('gpsi.staff.audit.car', 'audit_id', 'Action Requests')
    car_count = fields.Integer('Car Count', compute='_compute_car_count')
    notes = fields.Html('Notes')
    plan_ln_ids = fields.One2many('gpsi.staff.audit.plan.line', 'audit_id', 'Plan')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    ex_rpt_id = fields.Many2one(related='asst_id.ex_rpt_id')
    gn_rpt_id = fields.Many2one(related='asst_id.gn_rpt_id')

    @api.model
    def create(self, vals):
        res = super(Audit, self).create(vals)

        if res.chk_id and not res.asst_id:
            asst = res.chk_id.copy({'is_template': False})
            res.write({'asst_id': asst.id})

        return res

    @api.multi
    def name_get(self):
        return [(r.id, 'AU-{0:03d}'.format(r.id)) for r in self]

    @api.multi
    def _compute_car_count(self):
        """
        Calcula la cantidad de acciones correctivas
        """
        for audit in self:
            audit.car_count = len(audit.car_ids)

    @api.multi
    def _compute_auditor_id(self):
        for audit in self:
            lead =  audit.member_ids.find_lead()
            audit.auditor_id = lead and lead.id or False

    @api.multi
    def action_open_cars(self):
        self.ensure_one()
        return {
            "type": 'ir.actions.act_window',
            "res_model": 'gpsi.staff.audit.car',
            "views": [[False, 'tree'], [False, 'form']],
            "domain": [('audit_id', '=', self.id)],
            "context": {'default_audit_id': self.id},
            "name": "CAR'S",
        }

    @api.multi
    def action_open_asst_editor(self):
        """Abre una nueva ventana para editar la evaluación usando un sitio web personalizado
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/gpsi/staff/audits/{0}/assessment'.format(self.id),
            'target': 'new'
        }

    @api.multi
    def print_audit_executive_rpt(self):
        """Imprime el reporte executivo
        """
        self.ensure_one()
        return self.env['report'].get_action(self, self.ex_rpt_id.report_name)

    @api.multi
    def print_audit_general_rpt(self):
        """Imprime el reporte general
        """
        self.ensure_one()
        return self.env['report'].get_action(self, self.gn_rpt_id.report_name)


class Checklist(models.Model):
    """
    Checklist
    """
    _name = 'gpsi.staff.audit.chk'
    _description = 'Checklist'

    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)
    view_id = fields.Many2one('ir.ui.view', 'View', domain=[('type','=','qweb'), ('active','=',True)])
    gn_rpt_id = fields.Many2one('ir.actions.report.xml', 'General Report')
    ex_rpt_id = fields.Many2one('ir.actions.report.xml', 'Executive Report')
    field_ids = fields.One2many('gpsi.staff.audit.chk.field', 'chk_id', 'Fields')
    line_ids = fields.One2many('gpsi.staff.audit.chk.line', 'chk_id', 'Lines')
    is_template = fields.Boolean('Template')
    score_ids = fields.Many2many('gpsi.staff.audit.chk.score', 'gpsi_staff_chk_score_rel', 'chk_id', 'score_id', 'Checklists')
    score_id = fields.Many2one('gpsi.staff.audit.chk.score', 'Score', domain="[('chk_ids','=',id)]", copy=False)
    eval_action = fields.Many2one('ir.actions.server', 'Eval Action', help='Run action when checklist is saved')
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        res = super(Checklist, self).copy(default=default)

        for field in self.field_ids:
            field.copy({'chk_id': res.id})

        for line in self.line_ids:
            nline = line.copy({'chk_id': res.id}) 
            for field in line.field_ids:
                field.copy({'chk_ln_id': nline.id})

        return res

    @api.model
    def find_templates(self):
        return self.search([('is_template','=',True)])

    @api.multi
    def action_open_preview(self):
        """Abre una nueva ventana para editar la evaluación usando un sitio web personalizado
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/gpsi/staff/chks/{0}/preview'.format(self.id),
            'target': 'new'
        }


class ChecklistLine(models.Model):
    _name = 'gpsi.staff.audit.chk.line'
    _description = 'Checklist Line'    

    chk_id = fields.Many2one('gpsi.staff.audit.chk', 'Checklist')
    name = fields.Char('Title')
    help = fields.Text('Help')
    sequence = fields.Integer('Sequence')
    description = fields.Text('Description')
    field_ids = fields.One2many('gpsi.staff.audit.chk.field', 'chk_ln_id', 'Fields')
    tag_ids = fields.Many2many('gpsi.staff.audit.chk.line.tag', 'gpsi_staff_chk_line_tag_rel', 'line_id', 'tag_id', 'Tags')
    score_ids = fields.Many2many('gpsi.staff.audit.chk.score', 'gpsi_staff_chk_line_score_rel', 'line_id', 'score_id', 'Scores')
    score_id = fields.Many2one('gpsi.staff.audit.chk.score', 'Score', domain="[('line_ids','=',id)]", copy=False)

    @api.multi
    def duplicate(self):
        self.ensure_one()
        nline = self.copy({
            'description': None,
            'help': None
        })
        for field in self.field_ids:
            field.copy({'chk_line_id': nline.id})


class ChecklistLineTag(models.Model):
    _name = 'gpsi.staff.audit.chk.line.tag'
    _description = "Checklist Line Tag"

    name = fields.Char('Name')
    color = fields.Integer('Color Index')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    

class ChecklistField(models.Model):
    _name = 'gpsi.staff.audit.chk.field'
    _description = 'Checklist Field'

    name = fields.Char('Name')
    help = fields.Text('Help')
    chk_id = fields.Many2one('gpsi.staff.audit.chk', 'Checklist')
    chk_ln_id = fields.Many2one('gpsi.staff.audit.chk.line', 'Line')
    typ = fields.Selection(FIELD_TYPES, 'Type')
    label = fields.Char('Field Label')
    b_value = fields.Boolean('Bool Value')
    c_value = fields.Char('Char Value')
    i_value = fields.Integer('Int Value')
    f_value = fields.Float('Float Value')
    d_value = fields.Date('Date Value')
    t_value = fields.Text('Text Value')
    h_value = fields.Html('Html Value')


class ChecklistScore(models.Model):
    _name = 'gpsi.staff.audit.chk.score'
    _description = "Checklist Score"
    _rec_name = 'short_desc'

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')
    short_desc = fields.Char('Description', help='Short Description')
    line_ids = fields.Many2many('gpsi.staff.audit.chk.line', 'gpsi_staff_chk_line_score_rel', 'score_id', 'line_id', 'Lines')
    chk_ids = fields.Many2many('gpsi.staff.audit.chk', 'gpsi_staff_chk_score_rel', 'score_id', 'chk_id', 'Checklists')


class Member(models.Model):
    """
    Miembro del equipo de auditoría
    """
    _name = 'gpsi.staff.audit.member'
    _description = 'Audit Member'
    
    audit_id = fields.Many2one('gpsi.staff.audit', 'Audit')
    partner_id = fields.Many2one('res.partner', 'Auditor', domain=[('company_id','=',1)])
    role = fields.Many2one('gpsi.staff.audit.member.role', 'Role')

    @api.multi
    def find_lead(self):
        """
        Regresa el auditor lider del conjunto

        :return False si lider no es encontrado
        """
        role_lead = self.env.ref('gpsi_staff.audit_member_role_lead')
        for member in self:
            if member.role.id == role_lead.id:
                return member.partner_id
        return False


class MemberRole(models.Model):
    _name = 'gpsi.staff.audit.member.role'
    _description = 'Member Role'
    
    name = fields.Char('Name')


class Plan(models.Model):
    """
    Plan de auditoría
    """
    _name = 'gpsi.staff.audit.plan'


class PlanLine(models.Model):
    """
    Linea de plan de auditoría
    """
    _name = 'gpsi.staff.audit.plan.line'

    audit_id = fields.Many2one('gpsi.staff.audit', 'Audit')
    date = fields.Date('Date')
    hour = fields.Float('Hour')
    auditor_id = fields.Many2one('res.partner', 'Auditor', domain=[('company_id','=',1)])
    process = fields.Text('Process')


class CorrectiveActionReq(models.Model):
    """
    Corrective Action Request
    """
    _name = 'gpsi.staff.audit.car'
    _description = 'Corrective Action Request'
    _inherit = ['mail.thread']

    audit_id = fields.Many2one('gpsi.staff.audit', 'Audit')
    active = fields.Boolean('Active', default=True)
    due_date = fields.Date('Due Date')
    nonconformity = fields.Html('Nonconformity')
    correction = fields.Html('Inmediate Correction')
    root_cause = fields.Html('Root Cause Analysis')
    action_plan = fields.Html('Action Plans')
    conclusion = fields.Html('Conclusion')
    state = fields.Selection(CAR_STAGES, 'State', default=CAR_STAGES[0][0])

    @api.multi
    def name_get(self):
        return [(r.id, 'CAR-{0:03d}'.format(r.id)) for r in self]
