# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Globot(models.Model):
    _inherit = 'res.users'

    @api.multi
    def send_email_crm(self):
        self.ensure_one()

    @api.multi
    def _send_cert_application_crm(self):
        """Envia un email al cliente solicitando llene el formulario de aplicación"""
        self.ensure_one()

    @api.multi
    def _send_course_application_crm(self):
        """Envia un email al cliente solicitando llene el formulario de curso"""
        self.ensure_one()

    @api.multi
    def _process_cert_application_crm(self):
        self.ensure_one()

    @api.multi
    def find_busy_salesman(self):
        """Busca a los vendedores con menos rendimiento"""
        self.ensure_one()