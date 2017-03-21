# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError

from exception import AuditiiException


class User(models.Model):
    _inherit = 'res.users'

    is_gaudit = fields.Boolean(related="company_id.is_gaudit")

    @api.model
    def create_gaudit_owner(self, username, email, pw, company_id):
        """
        Crea usuario con acceso a GAudit como Owner

        :param username: nombre del usuario
        :param email: email del usuario
        :param pw: password
        :param company_id: identificador de la compañia a la que estará asociado el usuario
        """
        if self.search([('login','=',email)]):
            raise AuditiiException(AuditiiException.DUPLICATE_USER_EMAIL)

        user = self.sudo().create({
            'name': username,
            'login': email,
            'password': pw,
            'company_id': company_id,
            'company_ids': [(4, company_id, False)]
        })

        self.sudo().env.ref('gpsi_auditii.group_ga_owner').write({
            'users': [(4, user.id, 0)]
        })
        return user
        
    def is_owner(self):
        pass
