# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

SKILL_RATINGS = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High')
]


class Employee(models.Model):
    _inherit = 'hr.employee'

    gs_competence_ids = fields.One2many('gpsi.staff.competence', 'employee_id', 'Competences')
    doc_count = fields.Integer(compute='_get_doc_count', index=True)

    @api.multi
    def _get_doc_count(self):
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'hr.employee'), ('res_id', '=', self.id)])
        self.doc_count = len(attachments)

    @api.multi
    def attachment_tree_view(self):
        domain = [('res_model', '=', 'hr.employee'), ('res_id', '=', self.id)]

        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the tasks and issues of your project.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your project.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

class Competence(models.Model):
    _name = 'gpsi.staff.competence'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    skill_id = fields.Many2one('gpsi.staff.skill', 'Skill')
    rating = fields.Selection(SKILL_RATINGS, 'Rating', index=True, default=SKILL_RATINGS[0][0])

class Skill(models.Model):
    _name = 'gpsi.staff.skill'
    _parent_store = True
    _order = 'parent_left'

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
    parent_id = fields.Many2one('gpsi.staff.skill', 'Parent', ondelete='cascade')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many('gpsi.staff.skill', 'parent_id', 'Children')

    @api.multi
    def name_get(self):
        res = []
        for skill in self:
            names = []
            current = skill
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((skill.id, ' / '.join(reversed(names))))
        return res
