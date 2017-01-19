# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class EmployeeProfile(models.Model):
    '''
    Model para el perfil profesional del empleado.
    '''

    _name = 'hr.employee.profile'
    _description = 'Employee Profile'

    employee_id = fields.Many2one('hr.employee', 'Employee')
    customer_id = fields.Many2one('res.partner', 'Customer')
    work_history_ids = fields.One2many('hr.employee.profile.work.experiencie', 'experience_id', 'Work Experience')
    job_training_ids = fields.One2many('hr.employee.profile.job.training', 'training_id', 'Job Training')

class WorkExperience(models.Model):
    '''
    Model para listar experiencia laboral del empleado.
    '''

    _name = 'hr.employee.profile.work.experiencie'
    _descripcion = 'Work Experience'
    
    work_position = fields.Char('Professional Experience')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    experience_id = fields.Many2one('hr.employee.profile', 'Employee Profile', ondele="cascade")

class JobTraining(models.Model):
    '''
    Model para listar formación y conocimientos del empleado.
    '''

    _name = 'hr.employee.profile.job.training'
    _description = 'Job Training'

    expertise_area = fields.Char('Area of Expertise')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    training_id = fields.Many2one('hr.employee.profile', 'Employee Profile', ondele="cascade")

    











