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
    experience_ids = fields.One2many('hr.employee.profile.employment.experience', 'experience_id', 'Employment Experience')
    training_ids = fields.One2many('hr.employee.profile.job.training', 'training_id', 'Job Training')
    historial_ids = fields.One2many('hr.employee.profile.academic.historial', 'college_id', 'Academic Historial')
    courses_ids = fields.One2many('hr.employee.profile.completed.courses', 'course_id', 'Completed Courses')

class EmploymentExperience(models.Model):
    '''
    Model para listar experiencia laboral del empleado.
    '''

    _name = 'hr.employee.profile.employment.experience'
    _descripcion = 'Employment Experience'
    
    job_position = fields.Char('Job Position')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    experience_id = fields.Many2one('hr.employee.profile', 'Profile')

class JobTraining(models.Model):
    '''
    Model para listar formación y conocimientos del empleado.
    '''

    _name = 'hr.employee.profile.job.training'
    _description = 'Job Training'

    expertise_area = fields.Char('Area of Expertise')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    training_id = fields.Many2one('hr.employee.profile', 'Profile', ondele="cascade")

class AcademicHistorial(models.Model):
    '''
    Model para lista el historial académico del empleado.
    '''

    _name = 'hr.employee.profile.academic.historial'
    _description = 'Academic Historial'

    study_grade = fields.Char('Study Grade')
    institute = fields.Char('Alma Mater')
    start_date = fields.Date('End Date')
    end_date = fields.Date('End Date')
    college_id = fields.Many2one('hr.employee.profile', 'Profile', ondele="cascade")

class CompletedCourses(models.Model):
    '''
    Model para lista los cursos fianalizados por el empleado.
    '''

    _name = 'hr.employee.profile.completed.courses'
    _description = 'Completed Courses'

    course = fields.Char('Course')
    start_date = fields.Date('End Date')
    end_date = fields.Date('End Date')
    course_id = fields.Many2one('hr.employee.profile', 'Profile', ondele="cascade")



















