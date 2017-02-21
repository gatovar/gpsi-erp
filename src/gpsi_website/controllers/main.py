# -*- coding: utf-8 -*-

import logging
import werkzeug
import openerp

from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import Home

_logger = logging.getLogger(__name__)


class GlobalAuditAdminWebsite(http.Controller):
    @http.route('/ga/admin/signin', type='http', auth="none")
    def sign_in(self, redirect=None, **kw):
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate('demo', request.params['login'], request.params['password'])
            if uid is not False:
                request.params['login_success'] = True
                if not redirect:
                    redirect = '/ga/admin'
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        return request.render('gpsi_website.ga/admin/login', values)

    @http.route('/ga/admin/signup', type='http', methods=['POST'], auth="none")
    def sign_up(self, redirect=None, **kw):
        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None
        
        company = request.env['res.company'].sudo().create({
            'name': request.params['company'],
            'rml_header1': False,
            'email': request.params['email'],
            'currency_id': request.env['res.currency'].sudo().search([('name','=','USD')]).id
        })

        user = request.env['res.users'].sudo().create({
            'name': request.params['username'],
            'login': request.params['email'],
            'password': request.params['password'],
            'company_id': company.id,
            'company_ids': [(4, company.id, False)]
        })

        uid = request.session.authenticate('demo', request.params['email'], request.params['password'])
        if uid is not False:
            request.params['login_success'] = True
            if not redirect:
                redirect = '/ga/admin'
            return http.redirect_with_hash(redirect)

        return request.render('gpsi_website.ga/admin/login', values)

    @http.route('/ga/admin/logout', type='http', auth="user")
    def logout(self):
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect('/ga/admin/signin', 303)

    @http.route('/ga/admin', type='http', auth="user")
    def dashboard(self, **kw):
        return request.render('gpsi_website.ga/admin/dashboard')

    @http.route('/ga/admin/ca/contracts', type='http', auth="user")
    def ca_contracts(self, **kw):
        return request.render('gpsi_website.ca/contracts')

    @http.route('/ga/admin/ca/contracts/<int:contract_id>', type='http', auth="user")
    def ca_contract(self, contract_id, **kw):
        return request.render('gpsi_website.ca/contract')

    @http.route('/ga/admin/ca/events', type='http', auth="user")
    def ca_events(self, **kw):
        return request.render('gpsi_website.ca/events')

    @http.route('/ga/admin/ca/events/<int:event_id>', type='http', auth="user")
    def ca_event(self, event_id, **kw):
        return request.render('gpsi_website.ca/event')

    @http.route('/ga/admin/ca/reports/efficiency', type='http', auth="user")
    def ca_reports_efficiency(self, **kw):
        return request.render('gpsi_website.ca/reports/efficiency')

    @http.route('/ga/admin/va/suppliers', type='http', auth="user")
    def va_suppliers(self, **kw):
        suppliers = request.env['res.partner'].search([('parent_id','=',False), ('supplier','=',True)])
        qcontext = {
            'suppliers': suppliers
        }
        return request.render('gpsi_website.va/suppliers', qcontext)

    @http.route('/ga/admin/va/suppliers/new', type='http', auth="user")
    def va_supplier_new(self, **kw):
        return request.render('gpsi_website.va/supplier_new')

    @http.route('/ga/admin/va/suppliers/new', type='http', methods=['POST'], auth="user")
    def post_va_supplier_new(self, **kw):
        Partner = request.env['res.partner']
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
            'supplier': True
        })
        return werkzeug.utils.redirect('/ga/admin/va/suppliers/' + str(partner.id))

    @http.route('/ga/admin/va/suppliers/<int:supplier_id>', type='http', auth="user")
    def va_supplier(self, supplier_id, **kw):
        contact = request.env['res.partner'].search([('id','=',supplier_id)])
        qcontext = {
            'contact': contact
        }
        return request.render('gpsi_website.va/supplier', qcontext)

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
        Partner = request.env['res.partner']
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
            'customer': False
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
        project = request.env['project.project'].sudo().search([('gs_is_vendor_audit','=',True), ('partner_id','=',request.env.user.company_id.partner_id.id)])
        audits = request.env['project.task'].sudo().search([('project_id','=',project.id)], order='create_date desc')
        qcontext = {
            'audits': audits
        }
        return request.render('gpsi_website.va/events', qcontext)

    @http.route('/ga/admin/va/events/new', type='http', methods=['GET'], auth="user")
    def va_event_new(self, **kw):
        return request.render('gpsi_website.va/event_new')

    @http.route('/ga/admin/va/events/new', type='http', methods=['POST'], auth="user")
    def post_va_event_new(self, **kw):
        project = request.env['project.project'].sudo().search([('gs_is_vendor_audit','=',True), ('partner_id','=',request.env.user.company_id.partner_id.id)])
        auditee = request.env['res.partner'].sudo().search([('id','=',int(kw['supplier']))])
        Task = request.env['project.task'].sudo()
        audit = Task.create({
            'name': auditee.name,
            'project_id': project.id,
            'company_id': 1,
            'partner_id': int(kw['supplier']),
            'gs_checklist_id': int(kw['checklist']),
            'date_deadline': kw['date'],
            'description': kw['notes']
        })
        return werkzeug.utils.redirect('/ga/admin/va/events/' + str(audit.id))

    @http.route('/ga/admin/va/events/<int:event_id>', type='http', auth="user")
    def va_event(self, event_id, **kw):
        audit = request.env['project.task'].sudo().search([('id','=',event_id)])
        attachments = request.env['ir.attachment'].sudo().search([('res_model','=','project.task'), ('res_id','=',event_id)])
        stages = request.env['project.task.type'].sudo().search([('project_ids','in',[audit.project_id.id])])
        qcontext = {
            'audit': audit,
            'attachments': attachments,
            'stages': stages
        }
        return request.render('gpsi_website.va/event', qcontext)

    @http.route('/ga/admin/va/events/<int:event_id>/new_message', type='http', methods=['POST'], auth="user")
    def post_va_event_message(self, event_id, **kw):
        Task = request.env['project.task'].sudo()
        conversation = Task.search([('id','=',event_id)])
        conversation.message_post(body=kw['body'], message_type='comment', author_id=request.env.user.partner_id.id)
        
        return werkzeug.utils.redirect('/ga/admin/va/events/' + str(event_id) + '#add_comment')

    @http.route('/ga/admin/va/events/<int:event_id>/assessment', type='http', auth="user")
    def va_event_assessment(self, event_id, **kw):
        audit = request.env['project.task'].sudo().search([('id','=',event_id)])
        qcontext = {
            'editable': False,
            'audit': audit,
            'assessment': audit.gs_assessment_id
        }
        return request.render(audit.gs_assessment_id.view_id.xml_id, qcontext)

    @http.route('/ga/admin/va/events/<int:event_id>/assessment/edit', type='http', auth="user")
    def va_event_assessment_edit(self, event_id, **kw):
        audit = request.env['project.task'].sudo().search([('id','=',event_id)])
        qcontext = {
            'editable': True,
            'audit': audit,
            'assessment': audit.gs_assessment_id
        }
        return request.render(audit.gs_assessment_id.view_id.xml_id, qcontext)

    @http.route('/ga/admin/va/events/<int:event_id>/assessment/edit', methods=['POST'], type='http', auth="user")
    def post_va_event_assessment_edit(self, event_id, **kw):
        Line = request.env['gpsi.staff.checklist.line'].sudo()
        Field = request.env['gpsi.staff.checklist.field'].sudo()
        for key in kw:
            if 'field$$' in key:
                field = Field.search([('id','=',int(key[7:]))])
                if field.field_type == 'boolean':
                    field.write({'b_value': bool(kw[key])})
                elif field.field_type == 'char':
                    field.write({'c_value': kw[key]})
                elif field.field_type == 'int':
                    field.write({'i_value': int(kw[key])})
                elif field.field_type == 'float':
                    field.write({'f_value': float(kw[key])})
                elif field.field_type == 'date':
                    field.d_value = False
                elif field.field_type == 'text':
                    field.write({'t_value': kw[key]})
                elif field.field_type == 'html':
                    field.write({'h_value': kw[key]})
            if 'line_score_id$$' in key:
                line = Line.search([('id','=',int(key[15:]))])
                line.write({'score_id': int(kw[key])})

        return werkzeug.utils.redirect('/ga/admin/va/events/' + str(event_id) + '/assessment/edit')

    @http.route('/ga/admin/va/cars', type='http', auth="user")
    def va_cars(self, **kw):
        return request.render('gpsi_website.va/cars')

    @http.route('/ga/admin/va/cars/<int:car_id>', type='http', auth="user")
    def va_car(self, car_id, **kw):
        return request.render('gpsi_website.va/car')

    @http.route('/ga/admin/va/complaints', type='http', auth="user")
    def va_complaints(self, **kw):
        return request.render('gpsi_website.va/complaints')

    @http.route('/ga/admin/va/complaints/<int:complaint_id>', type='http', auth="user")
    def va_complaint(self, complaint_id, **kw):
        return request.render('gpsi_website.va/complaint')

    @http.route('/ga/admin/va/reports/efficiency', type='http', auth="user")
    def va_reports_efficiency(self, **kw):
        return request.render('gpsi_website.va/reports/efficiency')

    @http.route('/ga/admin/va/reports/complaints', type='http', auth="user")
    def va_reports_complaints(self, **kw):
        return request.render('gpsi_website.va/reports/complaints')

    @http.route('/ga/admin/clients/events', type='http', auth="user")
    def clients_events(self, **kw):
        audits = request.env['project.task'].sudo().search([('partner_id','=',request.env.user.partner_id.id)])
        qcontext = {
            'audits': audits
        }
        return request.render('gpsi_website.va/events', qcontext)

    @http.route('/ga/admin/settings/company', type='http', auth="user")
    def settings_company(self, **kw):
        return request.render('gpsi_website.settings/company')

    @http.route('/ga/admin/settings/users', type='http', auth="user")
    def settings_users(self, **kw):
        users = request.env['res.users'].sudo().search([('company_id','=',request.env.user.company_id.id)])
        qcontext = {
            'users': users
        }
        return request.render('gpsi_website.ga/admin/settings/users', qcontext)

    @http.route('/ga/admin/settings/users/<int:user_id>', type='http', auth="user")
    def settings_user(self, user_id, **kw):
        user = request.env['res.users'].sudo().search([('id','=',user_id)])
        qcontext = {
            'user': user
        }
        return request.render('gpsi_website.ga/admin/settings/user', qcontext)

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

        Group = request.env['res.groups'].sudo()
        owner_group = Group.search([('id','=',request.env.ref('gpsi_staff.group_ga_owner').id)])
        admin_group = Group.search([('id','=',request.env.ref('gpsi_staff.group_ga_admin').id)])
        user_group = Group.search([('id','=',request.env.ref('gpsi_staff.group_ga_user').id)])

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
        return request.render('gpsi_website.ga/admin/settings/user_new')

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
        return request.render('gpsi_website.settings/integrations')

    @http.route('/ga/admin/account/invoices/<int:invoice_id>', type='http', auth="user")
    def account_invoice(self, invoice_id, **kw):
        return request.render('gpsi_website.account/invoice')
