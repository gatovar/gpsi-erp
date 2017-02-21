Solicito una auditoría a un partner, se le envia una invitación, cuando la solicitud es aceptada entonces
el usuario que acepto la invitación es asociado a ese partner.

El partner debe tener un usuario relacionado.

class ResPartner:
    gs_user_id = fields.Many2one()
    gs_token = fields.Char()


class ResUsers:
    gs_partner_ids = fields.One2many()

De esa manera relaciono partner con usuarios...