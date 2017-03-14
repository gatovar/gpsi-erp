# -*- coding: utf-8 -*-

import uuid

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError


class AuditInvitation(models.Model):
    _name = 'gpsi.auditii.audit.invitation'
    _description = 'Audit Invitation'

    audit_task_id = fields.Many2one('project.task', 'Audit Task')
    token = fields.Char('Token', index=True)
    expiration_date = fields.Date('Expiration')
    active = fields.Boolean('Active', default=True)

    @api.model
    def send_invitation(self, auditee, audit_task_id, expiration_date=None):
        """
        Envia un correo al auditado notificandole que será parte de una
        auditoría.

        :param auditee: auditado
        :param audit_task_id: ID de la tarea de auditoría
        :param expiration_date: fecha de expiración de la invitación
        """
        token = uuid.uuid4().__str__()

        body = '''Apreciado {0},
        Has sido invitado a participar en un proceso de auditoría, favor de hacer clic en el siguiente link:
        http://192.168.99.100:8079/ga/admin/invitation?t={1}
        '''.format(auditee.name, token)

        self.sudo().create({
            'audit_task_id': audit_task_id,
            'token': token,
            'expiration_date': expiration_date
        })

        Mail = self.env['mail.mail']
        values = {
            'model': None,
            'res_id': None,
            'subject': 'Proceso de Auditoría',
            'body_html': body,
            'parent_id': None,
            'email_from': 'software@globalstd.com',
            'email_to': auditee.email,
            'auto_delete': True,
        }
        Mail.create(values).send()

    @api.model
    def find(self, token):
        """
        Busca invitación asociada al token dado.
        """
        return self.search([('token','=',token)])

    @api.model
    def accept_invitation(self, user, token):
        """
        Acepta la invitación asociada al token dado. Si no existe invitación para el 
        token, esta función regresa False, en caso contrario se asocia el proveedor de
        la auditoría solicitada con la compañia del usuario actual siempre y cuando
        esta no haya sido inicializada.

        :param token: usuario
        :param token: token
        """
        invitation = self.find(token)
        if not invitation:
            return False
        
        auditee = invitation.audit_task_id.audit_id.auditee_id
        if not auditee.gaudit_partner_id.aii_company_id:
            auditee.gaudit_partner_id.write({
                'aii_company_id': user.company_id.id
            })

        invitation.write({
            'active': False
        })

        user.company_id.add_customer_audit(invitation.audit_task_id)
        return True
