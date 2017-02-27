# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class Checklist(models.Model):
    _name = 'gpsi.staff.checklist'
    _description = 'Checklist'

    name = fields.Char('Name')
    view_id = fields.Many2one('ir.ui.view', 'View', domain=[('type','=','qweb'), ('active','=',True)])
    general_report_id = fields.Many2one('ir.ui.view', 'General Report', domain=[('type','=','qweb'), ('active','=',True)])
    executive_report_id = fields.Many2one('ir.ui.view', 'Executive Report', domain=[('type','=','qweb'), ('active','=',True)])
    field_ids = fields.One2many('gpsi.staff.checklist.field', 'checklist_id', 'Fields')
    line_ids = fields.One2many('gpsi.staff.checklist.line', 'checklist_id', 'Lines')
    is_template = fields.Boolean('Is Template?')
    rev = fields.Integer('Revision')
    active = fields.Boolean('Active', default=True)
    score_ids = fields.Many2many('gpsi.staff.checklist.score', 'gpsi_staff_checklist_score_rel', 'checklist_id', 'score_id', 'Checklists')
    score_id = fields.Many2one('gpsi.staff.checklist.score', 'Score', domain="[('checklist_ids','=',id)]", copy=False)
    # TODO remover campo code
    code = fields.Text('Python Code', help='Run code when checklist is saved.')
    eval_action = fields.Many2one('ir.actions.server', 'Eval Action', help='Run action when checklist is saved.')

    @api.multi
    def write(self, vals):
        res = super(Checklist, self).write(vals)
        for checklist in self:
            if checklist.eval_action:
                checklist.eval_action.run()
        return res

    def create_assessment(self):
        res = self.copy({'is_template': False})
        for field in self.field_ids:
            field.copy({'checklist_id': res.id})

        for line in self.line_ids:
            nline = line.copy({'checklist_id': res.id}) 
            for field in line.field_ids:
                field.copy({'checklist_line_id': nline.id})
        return res


class ChecklistLine(models.Model):
    _name = 'gpsi.staff.checklist.line'
    _description = 'Checklist Line'    

    checklist_id = fields.Many2one('gpsi.staff.checklist', 'Checklist')
    name = fields.Char('Title')
    description = fields.Text('Description')
    help = fields.Text('Help')
    sequence = fields.Integer('Sequence')
    field_ids = fields.One2many('gpsi.staff.checklist.field', 'checklist_line_id', 'Fields')
    tag_ids = fields.Many2many('gpsi.staff.checklist.line.tag', 'gpsi_staff_checklist_line_tag_rel', 'line_id', 'tag_id', 'Tags')
    score_ids = fields.Many2many('gpsi.staff.checklist.line.score', 'gpsi_staff_checklist_line_score_rel', 'line_id', 'score_id', 'Scores')
    score_id = fields.Many2one('gpsi.staff.checklist.line.score', 'Score', domain="[('line_ids','=',id)]", copy=False)

    @api.multi
    def duplicate(self):
        self.ensure_one()
        nline = self.copy({
            'description': None,
            'help': None
        })
        for field in self.field_ids:
            field.copy({'checklist_line_id': nline.id})


class ChecklistLineTag(models.Model):
    _name = 'gpsi.staff.checklist.line.tag'
    _description = "Tags"

    name = fields.Char('Name')
    color = fields.Integer('Color Index')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
    

class ChecklistField(models.Model):
    _name = 'gpsi.staff.checklist.field'
    _description = 'Field'

    name = fields.Char('Name')
    checklist_id = fields.Many2one('gpsi.staff.checklist', 'Checklist')
    checklist_line_id = fields.Many2one('gpsi.staff.checklist.line', 'Checklist')
    field_type = fields.Selection([('boolean', 'Boolean'), ('char', 'Char'), ('int', 'Integer'), ('float', 'Float'), ('date', 'Date'), ('text', 'Text'), ('html', 'Html')], 'Type')
    help = fields.Text('Help')
    field_description = fields.Char('Field Label')
    b_value = fields.Boolean('Value')
    c_value = fields.Char('Value')
    i_value = fields.Integer('Value')
    f_value = fields.Float('Value')
    d_value = fields.Date('Value')
    t_value = fields.Text('Value')
    h_value = fields.Html('Value')


class ChecklistLineScore(models.Model):
    _name = 'gpsi.staff.checklist.line.score'
    _description = "Line Score"

    name = fields.Char('Name')
    value = fields.Float('Value')
    sequence = fields.Integer('Sequence')
    line_ids = fields.Many2many('gpsi.staff.checklist.line.score', 'gpsi_staff_checklist_line_score_rel', 'score_id', 'line_id', 'Lines')


class ChecklistScore(models.Model):
    _name = 'gpsi.staff.checklist.score'
    _description = "Checklist Score"

    name = fields.Char('Name')
    value = fields.Float('Value')
    sequence = fields.Integer('Sequence')
    checklist_ids = fields.Many2many('gpsi.staff.checklist.score', 'gpsi_staff_checklist_score_rel', 'score_id', 'checklist_id', 'Checklists')
