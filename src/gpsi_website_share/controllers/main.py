# -*- coding: utf-8 -*-

import werkzeug.utils
import werkzeug.wrappers

import odoo
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
                      serialize_exception as _serialize_exception

from odoo.exceptions import AccessError
from odoo.addons.web.controllers.main import Home


class WebsiteShare(http.Controller):
    @http.route('/website/share', auth="none", website=True)
    def website_share(self, **kw):
        if not request.session.uid:
            request.session.authenticate(request.session.db, 'anonymous', 'anonymous')
        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid
        context = request.env['ir.http'].webclient_rendering_context()
        return request.render('gpsi_website_share.index', qcontext=context)


class HomeExtension(Home):
    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        user = request.env['res.users'].browse(request.session.uid)
        if user and user.is_anonymous():
            return werkzeug.utils.redirect('/web/login', 303)
        return super(HomeExtension, self).web_client(s_action, **kw)
