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
    summary = fields.Char('Certifications Summary')
    customer_ids = fields.One2many('hr.employee.profile.customers', 'client_id', 'Customer')
    experience_ids = fields.One2many('hr.employee.profile.experience', 'experience_id', 'Experience')
    education_ids = fields.One2many('hr.employee.profile.education', 'education_id', 'Education')

class EmployeeCustomers(models.Model):
    '''
    Model para listar empresas auditadas por el empleado.
    '''

    _name = 'hr.employee.profile.customers'
    _description = 'Employee Customers'

    company_id = fields.Many2one('res.partner', 'Profile')
    client_id = fields.Many2one('hr.employee.profile', 'Profile')

class EmployeeExperience(models.Model):
    '''
    Model para listar experiencia laboral del empleado.
    '''

    _name = 'hr.employee.profile.experience'
    _descripcion = 'Employee Experience'
    
    company_id = fields.Many2one('res.partner', 'Company')
    job_position = fields.Char('Position')
    job_description = fields.Char('Description')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    experience_id = fields.Many2one('hr.employee.profile', 'Profile')

class EmployeeEducation(models.Model):
    '''
    Model para lista el historial académico del empleado.
    '''

    _name = 'hr.employee.profile.education'
    _description = 'Employee Education'

    study_level = fields.Char('Study Grade')
    alma_mater = fields.Char('Alma Mater')
    start_date = fields.Date('End Date')
    end_date = fields.Date('End Date')
    education_id = fields.Many2one('hr.employee.profile', 'Profile', ondele="cascade")