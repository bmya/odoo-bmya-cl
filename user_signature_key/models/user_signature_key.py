# -*- coding: utf-8 -*-
from __future__ import print_function
import os, datetime
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)
try:
    from M2Crypto import X509 as M2X509
    from M2Crypto.EVP import MessageDigest
except ImportError:
    raise Warning('no pudo cargar M2Crypto')

try:
    from OpenSSL.crypto import *
except ImportError:
    raise Warning('no pudo cargar OpenSSL.crypto')

try:
    import base64
except ImportError:
    raise Warning('no pudo cargar base64')

try:
    import cStringIO
except ImportError:
    raise Warning('no pudo cargar cStringIO')

type_ = FILETYPE_PEM

zero_values = {
    "filename": "",
    "key_file": False,
    "dec_pass":"",
    "not_before": False,
    "not_after": False,
    "status": "unverified",
    "final_date": False,
    "subject_title": "",
    "subject_c": "",
    "subject_serial_number": "",
    "subject_common_name": "",
    "subject_email_address": "",
    "issuer_country": "",
    "issuer_serial_number": "",
    "issuer_common_name": "",
    "issuer_email_address": "",
    "issuer_organization": "",
    "cert_serial_number": "",
    "cert_signature_algor": "",
    "cert_version": "",
    "cert_hash": "",
    "private_key_bits": "",
    "private_key_check": "",
    "private_key_type": "",
    "cacert": "",
    "cert": "",
}

class userSignature(models.Model):
    # _name = 'user.signature.key'
    _inherit = 'res.users'

    def default_status(self):
        return 'unverified'

    def load_cert_m2pem(self, *args, **kwargs):
        _logger.info(self.filename)
        filecontent = base64.b64decode(self.key_file)
        # _logger.info(filecontent)
        cert = M2X509.load_cert(filecontent)
        # cert = M2X509.load_cert('newfile.crt.pem')
        _logger.info('version     ', cert.get_version())
        _logger.info('serial#     ', cert.get_serial_number())
        _logger.info('not before  ', cert.get_not_before())
        _logger.info('not after   ', cert.get_not_after())
        issuer = cert.get_issuer()
        _logger.info('issuer.C    ', repr(issuer.C))
        _logger.info('issuer.O    ', repr(issuer.O))
        _logger.info('issuer.OU   ', repr(issuer.OU))
        _logger.info('issuer.CN   ', repr(issuer.CN))
        _logger.info('issuer.Email', repr(issuer.Email))
        subject = cert.get_subject()
        _logger.info('subject.C', repr(subject.C))
        _logger.info('subject.CN', repr(subject.CN))
        _logger.info('subject.emailAddress', repr(subject.emailAddress))
        _logger.info('subject.serialNumber', repr(subject.serialNumber))
        _logger.info(cert.as_text(), '\n')

    def load_cert_pk12(self, filecontent):
        # _logger.info(filename)

        # p12 = load_pkcs12(file(filename, 'rb').read(), self.dec_pass)
        try:
            p12 = load_pkcs12(filecontent, self.dec_pass)
        except:
            raise Warning('Invalid Passphrase')

        #try:
        # p12 = load_pkcs12(output.read(), self.dec_pass)
        #except Exception as ex:
        #    raise Warning('Exception raised: %s' % ex)

        cert = p12.get_certificate()
        privky = p12.get_privatekey()
        cacert = p12.get_ca_certificates()
        issuer = cert.get_issuer()
        subject = cert.get_subject()

        self.not_before = datetime.datetime.strptime(cert.get_notBefore(), '%Y%m%d%H%M%SZ')
        self.not_after = datetime.datetime.strptime(cert.get_notAfter(), '%Y%m%d%H%M%SZ')
        _logger.info('not before           ', datetime.datetime.strptime(cert.get_notBefore(), '%Y%m%d%H%M%SZ'))
        _logger.info('not after            ', datetime.datetime.strptime(cert.get_notAfter(), '%Y%m%d%H%M%SZ'))

        # self.final_date =
        self.subject_c = subject.C
        self.subject_title = subject.title
        self.subject_common_name = subject.CN
        self.subject_serial_number = subject.serialNumber
        self.subject_email_address = subject.emailAddress

        _logger.info('subject.C            ', subject.C)
        _logger.info('subject.title        ', subject.title)
        _logger.info('subject.CN           ', subject.CN)
        _logger.info('subject.serialNumber ', subject.serialNumber)
        _logger.info('subject.emailAddress ', subject.emailAddress)

        self.issuer_country = issuer.C
        self.issuer_organization = issuer.O
        self.issuer_common_name = issuer.CN
        self.issuer_serial_number = issuer.serialNumber
        self.issuer_email_address = issuer.emailAddress
        self.status = 'expired' if cert.has_expired() else 'valid'

        _logger.info('issuer.C             ', issuer.C)
        _logger.info('issuer.O             ', issuer.O)
        _logger.info('issuer.CN            ', issuer.CN)
        _logger.info('issuer.serialNumber  ', issuer.serialNumber)
        _logger.info('issuer.emailAddress  ', issuer.emailAddress)


        _logger.info('expired?             ', cert.has_expired())
        _logger.info('name hash            ', cert.subject_name_hash())
        _logger.info('private key bits: ', privky.bits())
        # _logger.info('private key check: ', privky.check())
        # _logger.info('private key type: ', privky.type())
        _logger.info('cacert: ', cacert)
        _logger.info('xxx        ', cert)

        self.cert_serial_number = cert.get_serial_number()
        self.cert_signature_algor = cert.get_signature_algorithm()
        self.cert_version  = cert.get_version()
        self.cert_hash = cert.subject_name_hash()

        _logger.info('cert serial number   ', cert.get_serial_number())
        _logger.info('cert signature algor.', cert.get_signature_algorithm())
        _logger.info('cert version         ', cert.get_version())

        # data privada
        self.private_key_bits = privky.bits()
        # self.private_key_check = privky.check()
        # self.private_key_type = privky.type()
        # self.cacert = cacert

        certificate = p12.get_certificate()
        private_key = p12.get_privatekey()

        self.priv_key = dump_privatekey(type_, private_key)
        self.cert = dump_certificate(type_, certificate)

        pubkey = cert.get_pubkey()
        _logger.info('pubkeyyyyyyyyyyyyyyyyyyyyyyyyy!!!!!!!!')
        _logger.info(pubkey)


        _logger.info(cert.digest('md5'))
        _logger.info(cert.digest('sha1'))
        try:
            a = cert.sign(pubkey, 'sha1')
            _logger.info(a)
        except Exception as ex:
            _logger.info('Exception raised: %s' % ex)
            # raise Warning('Exception raised: %s' % ex)

    filename = fields.Char('File Name')
    key_file = fields.Binary(
        string='Signature File', required=False, store=True,
        help='Upload the Signature File')
    dec_pass = fields.Char('Pasword')
    # vigencia y estado
    not_before = fields.Date(
        string='Not Before', help='Not Before this Date', readonly=True)
    not_after = fields.Date(
        string='Not After', help='Not After this Date', readonly=True)
    status = fields.Selection(
        [('unverified', 'Unverified'), ('valid', 'Valid'), ('expired', 'Expired')],
        string='Status', default=default_status,
        help='''Draft: means it has not been checked yet.\nYou must press the\
"check" button.''')
    final_date = fields.Date(
        string='Last Date', help='Last Control Date', readonly=True)
    # sujeto
    subject_title = fields.Char('Subject Title', readonly=True)
    subject_c = fields.Char('Subject Country', readonly=True)
    subject_serial_number = fields.Char(
        'Subject Serial Number', readonly=True)
    subject_common_name = fields.Char(
        'Subject Common Name', readonly=True)
    subject_email_address = fields.Char(
        'Subject Email Address', readonly=True)
    # emisor
    issuer_country = fields.Char('Issuer Country', readonly=True)
    issuer_serial_number = fields.Char(
        'Issuer Serial Number', readonly=True)
    issuer_common_name = fields.Char(
        'Issuer Common Name', readonly=True)
    issuer_email_address = fields.Char(
        'Issuer Email Address', readonly=True)
    issuer_organization = fields.Char(
        'Issuer Organization', readonly=True)
    # data del certificado
    cert_serial_number = fields.Char('Serial Number', readonly=True)
    cert_signature_algor = fields.Char('Signature Algorithm', readonly=True)
    cert_version  = fields.Char('Version', readonly=True)
    cert_hash = fields.Char('Hash', readonly=True)
    # data privad, readonly=Truea
    private_key_bits = fields.Char('Private Key Bits', readonly=True)
    private_key_check = fields.Char('Private Key Check', readonly=True)
    private_key_type = fields.Char('Private Key Type', readonly=True)
    # cacert = fields.Char('CA Cert', readonly=True)
    cert = fields.Text('Certificate', readonly=True)
    priv_key = fields.Text('Private Key', readonly=True)
    authorized_users_ids = fields.One2many('res.users','cert_owner_id',
                                           string='Authorized Users')
    cert_owner_id = fields.Many2one('res.users', 'Certificate Owner',
                                    select=True, ondelete='cascade')

    invcert = fields.Boolean(
        'Certificate invisible',
        readonly=True, compute='_not_same_user')

    @api.multi
    def _not_same_user(self):
        for usr in self:
            if (usr.id == self.env.user.id):
                usr.invcert = False
            else:
                usr.invcert = True
            _logger.info(
                'usuario del registro: {}, usuario corriente: {}, invcert: \
{}'.format(usr.id, self.env.user.id, usr.invcert))

    @api.multi
    def action_clean1(self):
        self.ensure_one()
        # todo: debe lanzar un wizard que confirme si se limpia o no
        # self.status = 'unverified'
        self.write(zero_values)


    @api.multi
    def action_process(self):
        self.ensure_one()
        filecontent = base64.b64decode(self.key_file)
        # fname = 'cert_file.p12'
        # f = open(fname,'w')
        # f.write(filecontent)
        # f.close()
        self.load_cert_pk12(filecontent)

    @api.multi
    @api.depends('key_file')
    def _get_date(self):
        self.ensure_one()
        old_date = self.issued_date
        if self.key_file != None and self.status == 'unverified':
            _logger.info(self.key_file)
            self.issued_date = fields.datetime.now()
        else:
            _logger.info('valor antiguo de fecha')
            _logger.info(old_date)
            self.issued_date = old_date

    #@api.one
    #def _get_name(self):
    #    self.filename = self.filename


    #@api.multi
    #@api.depends('key_file')
    #def _get_name(self):
    #    # self.ensure_one()
    #    for x in self:
    #        old_name = x.name
    #        if x.key_file != None and x.status == 'unverified':
    #            if x.filename:
    #                x.name = '%s - %s' % (
    #                    x.filename.replace('.p12', ''),
    #                    datetime.strptime(
    #                        x.issued_date, '%Y-%m-%d %H:%M:%S').strftime(
    #                        '%Y/%m/%d %H:%M:%S'))
    #        else:
    #            _logger.info('valor antiguo de nombre')
    #            _logger.info(old_name)
    #            x.name = old_name
