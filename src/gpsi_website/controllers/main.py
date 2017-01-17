# -*- coding: utf-8 -*-

import werkzeug
import openerp

from openerp import http
from openerp.http import request
#from openerp.addons.web.controllers.main import Home


class Website(http.Controller):
    @http.route('/gs/signin', type='http', auth="none")
    def signin(self, **kw):
        return request.render('gpsi_website.signin')

    @http.route('/gs/signup', type='http', auth="none")
    def signup(self, **kw):
        return request.render('gpsi_website.signup')

    @http.route('/gs', type='http', auth="none")
    def home(self, **kw):
        return request.render('gpsi_website.home')
