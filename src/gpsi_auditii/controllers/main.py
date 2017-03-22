import logging
import werkzeug
import openerp

from ..models.exception import AuditiiException

from openerp import http
from openerp.http import request
from openerp.exceptions import ValidationError
from openerp.tools import safe_eval
from openerp.addons.web.controllers.main import Home

_logger = logging.getLogger(__name__)

DB_NAME = 'demo'


class HomeExtension(Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        if redirect and '/ga/admin' in redirect:
            redirect_url = '/ga/admin/signin?redirect={0}'.format(redirect)
            return werkzeug.utils.redirect(redirect_url, 303)
        return super(HomeExtension, self).web_login(redirect=redirect, kw=kw)


class AuditiiController(http.Controller):
    def has_perms(self):
        """Valida que el usuario tenga los permisos adecuados
        """
        return request.env.user.has_group('gpsi_auditii.group_ga_user')

    @http.route('/ga/admin/signin', type='http', auth="none")
    def sign_in(self, redirect=None, **kw):
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        values['redirect'] = redirect
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(DB_NAME, request.params['login'], request.params['password'])
            if uid is not False:
                request.params['login_success'] = True
                if not redirect:
                    redirect = '/ga/admin'
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        return request.render('gpsi_auditii.admin/login', values)

    @http.route('/ga/admin/signup', type='http', methods=['POST'], auth="none")
    def sign_up(self, redirect=None, **kw):
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None
        
        try:
            company = request.env['res.company'].create_gaudit(kw['company'], kw['email'])
            user = request.env['res.users'].create_gaudit_owner(kw['username'], kw['email'], kw['password'], company.id)
        except AuditiiException as e:
            values['create_error'] = "Email already exist!"
            values['creating_account'] = True

        uid = request.session.authenticate(DB_NAME, request.params['email'], request.params['password'])
        if uid is not False:
            request.params['login_success'] = True
            if not redirect:
                redirect = '/ga/admin'
            return http.redirect_with_hash(redirect)

        return request.render('gpsi_auditii.admin/login', values)

    @http.route('/ga/admin/logout', type='http', auth="user")
    def logout(self):
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect('/ga/admin/signin', 303)

    @http.route('/ga/admin/invitation', type='http', auth="user")
    def invitation(self, t=None):
        AuditInvitation = request.env['gpsi.auditii.audit.invitation'].sudo()
        invitation = AuditInvitation.find(t)
        if AuditInvitation.accept_invitation(request.env.user, t):
            return werkzeug.utils.redirect('/ga/admin/clients/events/{0}'.format(invitation.audit_task_id.id), 303)    
        return werkzeug.utils.redirect('/ga/admin', 303)

    @http.route('/ga/admin', type='http', auth="user")
    def dashboard(self, **kw):
        if not self.has_perms():
            return request.render('gpsi_auditii.admin/forbidden')

        return request.render('gpsi_auditii.admin/dashboard')

    @http.route('/ga/admin/ca/contracts', type='http', auth="user")
    def ca_contracts(self, **kw):
        if not self.has_perms():
            return request.render('gpsi_auditii.admin/forbidden')

        return request.render('gpsi_auditii.admin/ca/contracts')

    @http.route('/ga/admin/ca/contracts/<int:contract_id>', type='http', auth="user")
    def ca_contract(self, contract_id, **kw):
        if not self.has_perms():
            return request.render('gpsi_auditii.admin/forbidden')

        return request.render('gpsi_auditii.admin/ca/contract')

    @http.route('/ga/admin/ca/events', type='http', auth="user")
    def ca_events(self, **kw):
        if not self.has_perms():
            return request.render('gpsi_auditii.admin/forbidden')

        Project = request.env['project.project'].sudo()
        Task = request.env['project.task'].sudo()

        gstd_partner = request.env.user.company_id.partner_id.gstd_partner_id
        tasks = Task.search([('project_id','=',request.env.ref('gpsi_staff.project_cert_audit').id), ('partner_id','=',gstd_partner.id)], order='date_deadline desc')
        qcontext = {
            'tasks': tasks
        }
        return request.render('gpsi_auditii.admin/ca/events', qcontext)

    @http.route('/ga/admin/ca/events/<int:event_id>', type='http', auth="user")
    def ca_event(self, event_id, **kw):
        if not self.has_perms():
            return request.render('gpsi_auditii.admin/forbidden')

        Task = request.env['project.task'].sudo()
        Attachment = request.env['ir.attachment'].sudo()
        StageType = request.env['project.task.type'].sudo()

        task = Task.search([('id','=',event_id)])
        attachments = Attachment.search([('res_model','=','project.task'), ('res_id','=',event_id)])
        stages = StageType.search([('project_ids','in',[task.project_id.id])])
        qcontext = {
            'task': task,
            'attachments': attachments,
            'stages': stages
        }
        return request.render('gpsi_auditii.admin/ca/event', qcontext)

    @http.route('/ga/admin/ca/events/<int:event_id>/cars', type='http', auth="user")
    def ca_cars(self, event_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        qcontext = {
            'task': task,
            'audit': task.audit_id,
            'cars': task.audit_id.car_ids
        }
        return request.render('gpsi_auditii.admin/ca/cars', qcontext)

    @http.route('/ga/admin/ca/events/<int:event_id>/cars/<int:car_id>', type='http', methods=['GET'], auth="user")
    def ca_car(self, event_id, car_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        car = request.env['gpsi.staff.audit.car'].sudo().search([('id','=',car_id)])
        attachments = request.env['ir.attachment'].sudo().search([('res_model','=','gpsi.staff.audit.car'), ('res_id','=',car_id)])
        qcontext = {
            'task': task,
            'car': car,
            'attachments': attachments,
            'readonly': False
        }
        return request.render('gpsi_auditii.admin/ca/car', qcontext)

    @http.route('/ga/admin/ca/events/<int:event_id>/cars/<int:car_id>', type='http', methods=['POST'], auth="user")
    def post_ca_car(self, event_id, car_id, **kw):
        car = request.env['gpsi.staff.audit.car'].sudo().search([('id','=',car_id)])
        car.write(kw)
        return werkzeug.utils.redirect('/ga/admin/ca/events/{0}/cars/{1}'.format(int(event_id), int(car_id)))

    @http.route('/ga/admin/va/suppliers', type='http', auth="user")
    def va_suppliers(self, **kw):
        suppliers = request.env['res.partner'].search([('company_id','=',request.env.user.company_id.id), ('parent_id','=',False), ('supplier','=',True)])
        qcontext = {
            'suppliers': suppliers
        }
        return request.render('gpsi_auditii.admin/va/suppliers', qcontext)

    @http.route('/ga/admin/va/suppliers/new', type='http', auth="user")
    def va_supplier_new(self, **kw):
        return request.render('gpsi_auditii.admin/va/supplier_new')

    @http.route('/ga/admin/va/suppliers/new', type='http', methods=['POST'], auth="user")
    def post_va_supplier_new(self, **kw):
        Partner = request.env['res.partner'].sudo()
        partner = Partner.create({
            'name': kw['name'],
            'active': True,
            'company_type': 'company',
            'street': kw['street'],
            'street2': kw['street2'],
            'city': kw['city'],
            'state_id': int(kw['state']) if int(kw['state']) > 0 else False,
            'zip': kw['zip'],
            'country_id': int(kw['country']) if int(kw['country']) > 0 else False,
            'website': kw['website'],
            'phone': kw['phone'],
            'mobile': kw['mobile'],
            'email': kw['email'],
            'customer': False,
            'supplier': True,
            'company_id': request.env.user.company_id.id,
            'create_gstd_partner': True
        })
        return werkzeug.utils.redirect('/ga/admin/va/suppliers/' + str(partner.id))

    @http.route('/ga/admin/va/suppliers/<int:supplier_id>', type='http', auth="user")
    def va_supplier(self, supplier_id, **kw):
        contact = request.env['res.partner'].search([('id','=',supplier_id)])
        qcontext = {
            'contact': contact
        }
        return request.render('gpsi_auditii.admin/va/supplier', qcontext)

    @http.route('/ga/admin/va/suppliers/<int:supplier_id>', type='http', methods=['POST'], auth="user")
    def post_va_supplier(self, supplier_id, **kw):
        Partner = request.env['res.partner']
        partner = Partner.search([('id','=',supplier_id)])
        partner.write({
            'name': kw['name'],
            'company_type': 'company',
            'street': kw['street'],
            'street2': kw['street2'],
            'city': kw['city'],
            'state_id': int(kw['state']) if int(kw['state']) > 0 else False,
            'zip': kw['zip'],
            'country_id': int(kw['country']) if int(kw['country']) > 0 else False,
            'website': kw['website'],
            'phone': kw['phone'],
            'mobile': kw['mobile'],
            'email': kw['email']
        })
        return werkzeug.utils.redirect('/ga/admin/va/suppliers/' + str(partner.id))

    @http.route('/ga/admin/va/suppliers/<int:supplier_id>/contacts/new', type='http', methods=['POST'], auth="user")
    def post_va_supplier_contact_new(self, supplier_id, **kw):
        Partner = request.env['res.partner'].sudo()
        Partner.create({
            'name': kw['name'],
            'active': True,
            'parent_id': supplier_id,
            'company_type': 'person',
            'type': 'contact',
            'function': kw['function'],
            'title': kw['title'],
            'phone': kw['phone'],
            'mobile': kw['mobile'],
            'email': kw['email'],
            'comment': kw['comment'],
            'customer': False,
            'company_id': request.env.user.company_id.id
        })
        return werkzeug.utils.redirect('/ga/admin/va/suppliers/' + str(supplier_id))

    @http.route('/ga/admin/va/suppliers/<int:supplier_id>/contacts/<int:contact_id>', type='http', methods=['POST'], auth="user")
    def post_va_supplier_contact(self, supplier_id, contact_id, **kw):
        Partner = request.env['res.partner']
        partner = Partner.search([('id','=',contact_id)])
        partner.write({
            'name': kw['name'],
            'function': kw['function'],
            'title': kw['title'],
            'phone': kw['phone'],
            'mobile': kw['mobile'],
            'email': kw['email'],
            'comment': kw['comment']
        })
        return werkzeug.utils.redirect('/ga/admin/va/suppliers/' + str(supplier_id) + '#contact_' + str(contact_id))

    @http.route('/ga/admin/va/events', type='http', auth="user")
    def va_events(self, **kw):
        Project = request.env['project.project']
        tasks = Project.find_supplier_audits()
        qcontext = {
            'tasks': tasks 
        }
        return request.render('gpsi_auditii.admin/va/events', qcontext)

    @http.route('/ga/admin/va/events/new', type='http', methods=['GET'], auth="user")
    def va_event_new(self, **kw):
        return request.render('gpsi_auditii.admin/va/event_new')

    @http.route('/ga/admin/va/events/new', type='http', methods=['POST'], auth="user")
    def post_va_event_new(self, **kw):
        Project = request.env['project.project']
        audit = Project.request_audit(int(kw['supplier']), int(kw['checklist']), kw['date'], kw['notes'])
        return werkzeug.utils.redirect('/ga/admin/va/events/' + str(audit.id))

    @http.route('/ga/admin/va/events/<int:event_id>', type='http', auth="user")
    def va_event(self, event_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        attachments = request.env['ir.attachment'].sudo().search([('res_model','=','project.task'), ('res_id','=',event_id)])
        stages = request.env['project.task.type'].sudo().search([('project_ids','in',[task.project_id.id])])
        qcontext = {
            'task': task,
            'attachments': attachments,
            'stages': stages
        }
        return request.render('gpsi_auditii.admin/va/event', qcontext)

    @http.route('/ga/admin/new_message', type='http', methods=['POST'], auth="user")
    def post_new_message(self, **kw):
        rec = request.env[kw['model']].sudo().search([('id','=',int(kw['id']))])
        rec.message_post(body=kw['body'], message_type='comment', author_id=request.env.user.partner_id.id)
        return werkzeug.utils.redirect('{0}#comments'.format(kw['redirect']))

    @http.route('/ga/admin/va/events/<int:event_id>/assessment', type='http', auth="user")
    def va_event_assessment(self, event_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        qcontext = {
            'readonly': True,
            'audit': task.audit_id,
            'assessment': task.audit_id.asst_id
        }
        return request.render(task.audit_id.asst_id.view_id.xml_id, qcontext)

    @http.route('/ga/admin/va/events/<int:event_id>/report/<string:type>', type='http', methods=['GET'], auth="user")
    def va_event_report(self, event_id, type, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        if type == 'executive':
            pdf = request.env['report'].sudo().get_pdf(task.audit_id, task.audit_id.ex_rpt_id.report_name)
        else:
            pdf = request.env['report'].sudo().get_pdf(task.audit_id, task.audit_id.gn_rpt_id.report_name)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route('/ga/admin/va/events/<int:event_id>/cars', type='http', auth="user")
    def va_cars(self, event_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        qcontext = {
            'task': task,
            'audit': task.audit_id,
            'cars': task.audit_id.car_ids
        }
        return request.render('gpsi_auditii.admin/va/cars', qcontext)

    @http.route('/ga/admin/va/events/<int:event_id>/cars/<int:car_id>', type='http', methods=['GET'], auth="user")
    def va_car(self, event_id, car_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        car = request.env['gpsi.staff.audit.car'].sudo().search([('id','=',car_id)])
        attachments = request.env['ir.attachment'].sudo().search([('res_model','=','gpsi.staff.audit.car'), ('res_id','=',car_id)])
        qcontext = {
            'task': task,
            'car': car,
            'attachments': attachments,
            'readonly': False
        }
        template = 'gpsi_auditii.admin/va/car'
        if task.partner_id.id == request.env.user.company_id.partner_id.gstd_partner_id.id:
            template = 'gpsi_auditii.admin/va/car2'
        return request.render(template, qcontext)

    @http.route('/ga/admin/va/events/<int:event_id>/cars/<int:car_id>', type='http', methods=['POST'], auth="user")
    def post_va_car(self, event_id, car_id, **kw):
        car = request.env['gpsi.staff.audit.car'].sudo().search([('id','=',car_id)])
        car.write(kw)
        return werkzeug.utils.redirect('/ga/admin/va/events/{0}/cars/{1}'.format(int(event_id), int(car_id)))

    @http.route('/ga/admin/clients/events', type='http', auth="user")
    def clients_events(self, **kw):
        tasks = request.env.user.company_id.cust_audit_task_ids
        qcontext = {
            'tasks': tasks
        }
        return request.render('gpsi_auditii.admin/clients/events', qcontext)

    @http.route('/ga/admin/clients/events/<int:event_id>', type='http', auth="user")
    def clients_event(self, event_id, **kw):
        task = request.env['project.task'].sudo().search([('id','=',event_id)])
        attachments = request.env['ir.attachment'].sudo().search([('res_model','=','project.task'), ('res_id','=',event_id)])
        stages = request.env['project.task.type'].sudo().search([('project_ids','in',[task.project_id.id])])
        qcontext = {
            'task': task,
            'audit': task.audit_id,
            'attachments': attachments,
            'stages': stages
        }
        return request.render('gpsi_auditii.admin/clients/event', qcontext)

    @http.route('/ga/admin/va/reports/efficiency', type='http', auth="user")
    def va_reports_efficiency(self, **kw):
        return request.render('gpsi_auditii.admin/va/reports/efficiency')

    @http.route('/ga/admin/va/reports/complaints', type='http', auth="user")
    def va_reports_complaints(self, **kw):
        return request.render('gpsi_auditii.admin/va/reports/complaints')

    @http.route('/ga/admin/settings/users', type='http', auth="user")
    def settings_users(self, **kw):
        users = request.env['res.users'].sudo().search([('company_id','=',request.env.user.company_id.id)])
        qcontext = {
            'users': users
        }
        return request.render('gpsi_auditii.admin/settings/users', qcontext)

    @http.route('/ga/admin/settings/users/<int:user_id>', type='http', auth="user")
    def settings_user(self, user_id, **kw):
        user = request.env['res.users'].sudo().search([('id','=',user_id)])
        qcontext = {
            'user': user
        }
        return request.render('gpsi_auditii.admin/settings/user', qcontext)

    @http.route('/ga/admin/settings/users/<int:user_id>', type='http', methods=['POST'], auth="user")
    def post_settings_user(self, user_id, **kw):
        user = request.env['res.users'].sudo().search([('id','=',user_id)])
        user.write({
            'name': kw['name'],
            'login': kw['login']
        })
        user.partner_id.write({
            'street': kw['street'],
            'street2': kw['street2'],
            'city': kw['city'],
            'state_id': int(kw['state']) if int(kw['state']) > 0 else False,
            'zip': kw['zip'],
            'country_id': int(kw['country']) if int(kw['country']) > 0 else False,
            'phone': kw['phone'],
            'mobile': kw['mobile']
        })

        if not user.has_group('gpsi_auditii.group_ga_owner'):
            Group = request.env['res.groups'].sudo()
            owner_group = Group.search([('id','=',request.env.ref('gpsi_auditii.group_ga_owner').id)])
            admin_group = Group.search([('id','=',request.env.ref('gpsi_auditii.group_ga_admin').id)])
            user_group = Group.search([('id','=',request.env.ref('gpsi_auditii.group_ga_user').id)])

            owner_group.write({'users': [(3, user_id, 0)]})
            admin_group.write({'users': [(3, user_id, 0)]})
            user_group.write({'users': [(3, user_id, 0)]})

            if kw['role'] == 'user':
                user_group.write({'users': [(4, user_id, 0)]})
            elif kw['role'] == 'admin':
                admin_group.write({'users': [(4, user_id, 0)]})
            elif kw['owner'] == 'admin':
                owner_group.write({'users': [(4, user_id, 0)]})
            
        return werkzeug.utils.redirect('/ga/admin/settings/users/' + str(user.id))

    @http.route('/ga/admin/settings/users/new', type='http', auth="user")
    def settings_user_new(self, **kw):
        return request.render('gpsi_auditii.admin/settings/user_new')

    @http.route('/ga/admin/settings/users/new', type='http', methods=['POST'], auth="user")
    def post_settings_user_new(self, **kw):
        User = request.env['res.users'].sudo()
        user = User.create({
            'name': kw['name'],
            'login': kw['login'],
            'company_id': request.env.user.company_id.id,
            'company_ids': [(4, request.env.user.company_id.id, False)]
        })
        user.partner_id.write({
            'street': kw['street'],
            'street2': kw['street2'],
            'city': kw['city'],
            'state_id': int(kw['state']) if int(kw['state']) > 0 else False,
            'zip': kw['zip'],
            'country_id': int(kw['country']) if int(kw['country']) > 0 else False,
            'phone': kw['phone'],
            'mobile': kw['mobile']
        })
        return werkzeug.utils.redirect('/ga/admin/settings/users/' + str(user.id))

    @http.route('/ga/admin/settings/integrations', type='http', auth="user")
    def settings_integrations(self, **kw):
        return request.render('gpsi_auditii.admin/settings/integrations')

