# -*- coding: utf-8 -*-
from openerp import fields, api, models, _
import time, md5
from datetime import datetime, timedelta
from openerp.exceptions import Warning
import os, sys, json
try:
    import urllib3
except ImportError:
    pass

import logging

http = urllib3.PoolManager()

_logger = logging.getLogger(__name__)

available_format = [
    ('JSON', 'JSON'),
    ('XML', 'XML'),
    ('HTML', 'HTML')
]

class webservices_generic(models.Model):
    _name = "webservices.server"
    
    
    @api.multi
    def action_test_connection(self):
        self.ensure_one()
        rr = self.generic_connection()
        # analiza la respuesta
        try:
            _logger.info('status %s' % (r.status))
        except:
            _logger.warning('exception status')

        _logger.warning(
                    'Expecting %s response format...' % self.response_format)
        if rr['status'] == 200:
            print rr['data']
            raise Warning(_('Result: %s!' % json.dumps(rr['data'])))
        else:
            raise Warning(_('Result: %s!' % rr['data']))


    def generic_connection(self):
        _logger.warning('Entering function "test connection"')
        base_url = self.url
        
        # token en el ecabezado (por ejemplo toggl)
        if self.auth_method == 'headers_token':
            _logger.warning('Entering headers_token method')
            connection = base_url
            headers = urllib3.util.make_headers(
                basic_auth='%s:api_token' % (self.token))
            r = http.request('GET', connection, headers=headers)
        
        # token junto con los datos (por ejemplo sbif)
        elif self.auth_method == 'data_token':
            headers={}
            _logger.info('entra por metodo data_token')
            
            connection = '{}?{}={}&{}={}'.format(
                self.url, self.auth_method_name, self.token,
                self.response_format_name, self.response_format)
            
            _logger.info('conection: %s' % connection)
            
        # esquema de datos complejo (no funciona) por ejemplo, Sugarcrm
        elif self.auth_method == 'user_password':
            headers={'Content-Type': 'application/json'}
            parameters = {'user_auth': {
                'user_name': self.user,
                'password': md5.new(self.password).hexdigest(),
                'version' : '1'
            }}
            print parameters
            connection = {
                "method" : "login",
                "input_type" : "JSON",
                "response_type" : "JSON",
                "rest_data" : parameters,
                "application_name":"RestTest",
                "name_value_list":""
            }

        # realiza la conexión
        print 'datos que envia', connection
        r = http.urlopen(self.http_auth_method, connection, headers=headers)
        _logger.info('encabezados de respuesta: %s' % r.headers)
        _logger.info('datos de la respuesta: %s' % r.data)
        rr = {}
        rr['headers'] = r.headers
        rr['status'] = r.status
        if r.status == 200:
            if self.response_format == 'JSON':
                rr['data'] = json.loads(r.data)
                _logger.info('formato json, status 200')
            else:
                # para trabajar con otros formatos de respuesta (no implementado)
                rr['data'] = r.data
                _logger.warning('formato json, status: %s' % r.status)
        else:
            rr['data'] = r.data
            _logger.warning('formato NO json, status: %s' % r.status)
        return rr
        

    
    name = fields.Char('Name', required=True)

    auth_method = fields.Selection(
        [
            ('headers_token', 'Token sent in header'),
            ('data_token', 'Token sent as part of dataset'),
            ('headers_key', 'Authentication Key sent in header'),
            ('user_password', 'User and password (get token)'),
        ], 'Auth Method',
        help="""Defines the authentication method used by the webservice""")

    http_auth_method = fields.Selection(
        [
            ('GET','GET'),
            ('POST','POST'),
            ('PUT','PUT')
        ], 'HTTP Method (auth)',
        help="""Defines the http method used for authentication""")

    auth_method_name = fields.Char('Auth Method Name')

    user_var = fields.Char('User Param. Name')

    user = fields.Char('User')

    password_var = fields.Char('Password Param. Name')

    password = fields.Char('Password')

    url = fields.Char('URL')

    just_url = fields.Boolean('Test URL only')

    token = fields.Char('Token')

    active = fields.Boolean('Active', default=True)

    custom_library = fields.Selection(
        [
            ('','Nope'),
            ('Y','Yes, Own URL'),
            ('P','Yes, Public URL'),
        ],
        'Third party library',
        help="""Defines if connection is made over standard libraries or 
third parties libraries, as, for example: 'Sugarcrm (own url)' or 'Mandrill'
(mandrill url included in module)""")

    scope = fields.Selection(
        [
            ('generic', 'Generic Use'),
            ('by_user', 'Use by user: each user has its own key')
        ],'Scope Use', help="""Defines Security Scope of use of the service
Generic Use: one service for all with Odoo Security
User by user: each user has its own key/token
        """,
        required=True)

    # request_format_name = fields.Char('Request Format Name')
    
    # request_format = fields.Selection(available_format, 'Request Format',
    #    help='Defines Expected Response Format', required=True, default='JSON')
    
    response_format_name = fields.Char('Response Format Name')
    
    response_format = fields.Selection(available_format, 'Response Format',
        help='Defines Expected Response Format', required=True, default='JSON')
    
    additional_parameter = fields.Char('Additional Parameter Name for Format',
        help="""Just provide the parameter_name required by the server to 
specify the desired format (i.e: &parameter_name='JSON')""")
    
    srv_users_ids = fields.One2many(
        'ws.srv.users', 'ws_server_id', string='Webservice Users')


class ws_srv_users(models.Model):
    _name = "ws.srv.users"

    name = fields.Char(
        'User Name',
        required=True,
        )
    usr_id = fields.Char(
        'User ID',
        )
    ws_server_id = fields.Many2one(
        'webservices.server', 'Webservices Server', select=True,
        ondelete='cascade')
    user_id = fields.Many2one(
        'res.users', 'User', select=True, ondelete='cascade')
