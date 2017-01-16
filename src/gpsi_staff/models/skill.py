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

class Attachments(models.Model):
    _inherit = 'ir.attachment'

    tags_ids = fields.Many2many('ir.attachment.category', string='Tags')

class AttachmentCategory(models.Model):
    _name = "ir.attachment.category"
    _description = "Attachment Category"

    name = fields.Char("Attachment Tag", required=True)
    color = fields.Integer('Color Index')
    tags_ids = fields.Many2many('ir.attachment', string='Tags')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

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
