# -*- coding: utf-8 -*-
from __future__ import print_function
import os, datetime

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning
# import io
from openerp import SUPERUSER_ID

try:
	from M2Crypto import X509 as M2X509
	from M2Crypto.EVP import MessageDigest
	from OpenSSL.crypto import *
    import base64
except ImportError:
    pass


class user_signature(models.Model):

    _name = 'user.signature.key'
    _inherit = 'res.users'

	def load_cert_pypk12():
	    # openssl
	    p12 = load_pkcs12(file('exportadodeChrome.p12', 'rb').read(), 'Escondida12')
	    cert = p12.get_certificate()
	    privky = p12.get_privatekey()
	    cacert = p12.get_ca_certificates()

	    issuer = cert.get_issuer()
	    subject = cert.get_subject()


	    # print('issuer               ', issuer)
	    print('issuer.C             ', issuer.C)
	    print('issuer.O             ', issuer.O)
	    print('issuer.CN            ', issuer.CN)
	    print('issuer.emailAddress  ', issuer.emailAddress)
	    print('issuer.serialNumber  ', issuer.serialNumber)

	    print('not before           ',datetime.datetime.strptime(cert.get_notBefore(), '%Y%m%d%H%M%SZ'))
	    print('not after            ',datetime.datetime.strptime(cert.get_notAfter(), '%Y%m%d%H%M%SZ'))

	    # print('subject              ', subject)
	    print('subject.C            ', subject.C)
	    print('subject.title        ', subject.title)
	    print('subject.CN           ', subject.CN)
	    print('subject.emailAddress ', subject.emailAddress)
	    print('subject.serialNumber ', subject.serialNumber)

	    print('cert serial number   ', cert.get_serial_number())
	    print('cert signature algor.', cert.get_signature_algorithm())
	    print('cert version         ', cert.get_version())
	    print('expired?             ', cert.has_expired())
	    print('name hash            ', cert.subject_name_hash())

	    print('private key bits: ', privky.bits())
	    print('private key check: ', privky.check())
	    print('private key type: ', privky.type())
	    print('cacert: ', cacert)

	    print('xxx        ', cert)

	    pubkey = cert.get_pubkey()

	    print(cert.digest('md5'))
	    print(cert.digest('sha1'))

	    a = cert.sign(pubkey, "sha1")
	    print(a)

	def load_cert_m2pem():
	    cert = M2X509.load_cert('newfile.crt.pem')

	    print('version     ', cert.get_version())
	    print('serial#     ', cert.get_serial_number())
	    print('not before  ', cert.get_not_before())
	    print('not after   ', cert.get_not_after())
	    issuer = cert.get_issuer()
	    #print('issuer      ', issuer)
	    print('issuer.C    ', repr(issuer.C))
	    print('issuer.O    ', repr(issuer.O))
	    print('issuer.OU   ', repr(issuer.OU))
	    print('issuer.CN   ', repr(issuer.CN))
	    print('issuer.Email', repr(issuer.Email))
	    subject = cert.get_subject()
	    print('subject.C', repr(subject.C))
	    print('subject.CN', repr(subject.CN))
	    print('subject.emailAddress', repr(subject.emailAddress))
	    print('subject.serialNumber', repr(subject.serialNumber))

	    print(cert.as_text(), '\n')


    file_name = fields.Char('File Name', readonly=True, compute='_get_name',
                       store=True)
    filename = fields.Char('File Name')
    key_file = fields.Binary(
        string='Clock Records File', filters='*.xls', required=True,
        store=True, help='Upload the XLS Clock File in this holder')
    dec_pass = fields.Password('Pasword')
    not_before = fields.Date(
        string='Not Before', help='Not Before this Date')
    not_after = fields.Date(
        string='Not After', help='Not After this Date')
    status = fields.Selection([('draft', 'Draft'),('valid', 'Valid'),
                               ('expired', 'Expired')],
                          string='Status', default='draft',
                          help='''Draft: means it has not been checked yet.
You must press the \"check"\ button.''')
    final_date = fields.Date(
        string='Last Date', help='Last Control Date')
	subject_title = fields.Char('Subject Title')
	subject_c = fields.Char('Subject Country')
	subject_serial_number = fields.Char('Subject Serial Number')
	subject_common_name = fields.Char('Subject Common Name')
	subject_email_address = fields.Char('Subject Email Address')
	issuer_country = fields.Char('Issuer Country')
	issuer_serial_number = fields.Char('Issuer Serial Number')
	issuer_common_name = fields.Char('Issuer Common Name')
	issuer_email_address = fields.Char('Issuer Email Address')
	issuer_organization = fields.Char('Issuer Organization')

	'''
    authorized_user_ids = fields.Many2many(
        'res.users', 'clock_record_id', string='Authorized Users')
	'''

    @api.multi
    def action_process(self):
        if 1 == 1:
            self.ensure_one()

            filecontent = base64.b64decode(self.clock_file)
            # ......aca va todo el codigo de proceso
        else:
            pass

    @api.multi
    def action_cancel(self):
        try:
            self.ensure_one()
            print('aca se cancela el archivo')
            self.status = 'cancelled'
        except:
            pass

    @api.multi
    @api.depends('clock_file')
    def _get_date(self):
        self.ensure_one()
        old_date = self.issued_date
        if self.clock_file != None and self.status == 'draft':
            print(self.clock_file)
            self.issued_date = fields.datetime.now()
        else:
            print('valor antiguo de fecha')
            print(old_date)
            self.issued_date = old_date



    @api.multi
    @api.depends('clock_file')
    def _get_name(self):
        self.ensure_one()
        old_name = self.name
        if self.clock_file != None and self.status == 'draft':
            if self.filename:
                self.name = '%s - %s' % (
                    self.filename.replace('.xls', ''), datetime.strptime(
                        self.issued_date, '%Y-%m-%d %H:%M:%S').strftime(
                        '%Y/%m/%d %H:%M:%S'))
        else:
            print('valor antiguo de nombre')
            print(old_name)
            self.name = old_name

'''
	def demo1():
	    print('Test 1: As DER...')
	    cert1 = M2X509.load_cert('newfile.crt.pem')
	    der1 = cert1.as_der()
	    dgst1 = MessageDigest('sha1')
	    dgst1.update(der1)
	    print('Using M2Crypto:\n', repr(dgst1.final()), '\n')

	    # cert2 = os.popen('openssl x509 -inform pem -outform der -in newfile.crt.pem')
	    # der2 = cert2.read()
	    # dgst2 = MessageDigest('sha1')
	    # dgst2.update(der2)
	    # print('Openssl command line:\n', repr(dgst2.final()), '\n')
'''

