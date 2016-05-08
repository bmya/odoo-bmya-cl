# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _
from openerp.exceptions import Warning
import logging
import lxml.etree as etree

import collections
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

# ejemplo de suds
import traceback as tb
import suds.metrics as metrics
#from tests import *
#from suds import WebFault
#from suds.client import Client
from suds.sax.text import Raw
import suds.client as sudscl
# ejemplo de suds

# intento con urllib3
import urllib3
pool = urllib3.PoolManager()

from inspect import currentframe, getframeinfo
# estas 2 lineas son para imprimir el numero de linea del script
# (solo para debug)

_logger = logging.getLogger(__name__)

try:
    import xmltodict
except ImportError:
    _logger.info('Cannot import xmltodict library')

try:
    import dicttoxml
except ImportError:
    _logger.info('Cannot import dicttoxml library')

try:
    from elaphe import barcode
except ImportError:
    _logger.info('Cannot import elaphe library')

try:
    import M2Crypto
except ImportError:
    _logger.info('Cannot import M2Crypto library')

try:
    import base64
except ImportError:
    _logger.info('Cannot import base64 library')

try:
    import hashlib
except ImportError:
    _logger.info('Cannot import hashlib library')

try:
    import cchardet
except ImportError:
    _logger.info('Cannot import hashlib library')

# timbre patrón. Permite parsear y formar el
# ordered-dict patrón corespondiente al documento
timbre  = """<TED version="1.0"><DD><RE>99999999-9</RE><TD>11</TD><F>1</F>\
<FE>2000-01-01</FE><RR>99999999-9</RR><RSR>\
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</RSR><MNT>10000</MNT><IT1>IIIIIII\
</IT1><CAF version="1.0"><DA><RE>99999999-9</RE><RS>YYYYYYYYYYYYYYY</RS>\
<TD>10</TD><RNG><D>1</D><H>1000</H></RNG><FA>2000-01-01</FA><RSAPK><M>\
DJKFFDJKJKDJFKDJFKDJFKDJKDnbUNTAi2IaDdtAndm2p5udoqFiw==</M><E>Aw==</E></RSAPK>\
<IDK>300</IDK></DA><FRMA algoritmo="SHA1withRSA">\
J1u5/1VbPF6ASXkKoMOF0Bb9EYGVzQ1AMawDNOy0xSuAMpkyQe3yoGFthdKVK4JaypQ/F8\
afeqWjiRVMvV4+s4Q==</FRMA></CAF><TSTED>2014-04-24T12:02:20</TSTED></DD>\
<FRMT algoritmo="SHA1withRSA">jiuOQHXXcuwdpj8c510EZrCCw+pfTVGTT7obWm/\
fHlAa7j08Xff95Yb2zg31sJt6lMjSKdOK+PQp25clZuECig==</FRMT></TED>"""
result = xmltodict.parse(timbre)
# result es un OrderedDict patrón
# hardcodeamos este valor por ahora


class invoice(models.Model):
    _inherit = "account.invoice"

    def whatisthis(self, s):
        if isinstance(s, str):
            print
            "ordinary string"
        elif isinstance(s, unicode):
            print
            "unicode string"
        else:
            print
            "not a string"

    def get_digital_signature(self):
        print('entro en digital signature function!!!!!')
        user_obj = self.env['res.users'].browse([self.env.user.id])
        signature_data = {
            'subject_name': user_obj.name,
            'subject_serial_number': user_obj.subject_serial_number,
            'priv_key': user_obj.priv_key,
            'cert': user_obj.cert.replace(
                '''-----BEGIN CERTIFICATE-----\n''','').replace(
                '''\n-----END CERTIFICATE-----\n''','')}
        print(signature_data)
        # todo: chequear si el usuario no tiene firma, si esta autorizado por otro usuario
        return signature_data

    def get_resolution_data(self, comp_id):
        print('get_resolution_data')
        print(comp_id)
        if comp_id.dte_service_provider == 'SIIHOMO':
            resolution_date = '2016-03-01'
            resolution_numb = '82'
        else:
            resolution_date = comp_id.dte_resolution_date
            resolution_numb = comp_id.dte_resolution_number
        resolution_data = {
            'dte_resolution_date': resolution_date,
            'dte_resolution_number': resolution_numb}
        return resolution_data

    @api.multi
    def send_xml_file(self):
        print('entro a la funcionnnnnnnnnnnn')
        print(self.company_id)
        print(self.company_id.dte_service_provider)

        if self.company_id.dte_service_provider == 'EFACTURADELSUR':
            # haciendolo para efacturadelsur solamente por ahora
            host = 'https://www.efacturadelsur.cl'
            post = '/ws/DTE.asmx' # HTTP/1.1
            url = host + post
            _logger.info('URL to be used %s' % url)
            # client = Client(url)
            # _logger.info(client)
            _logger.info('len (como viene): %s' % len(self.sii_xml_request))

            response = pool.urlopen('POST', url, headers={
                'Content-Type': 'application/soap+xml',
                'charset': 'utf-8',
                'Content-Length': len(
                    self.sii_xml_request)}, body=self.sii_xml_request)

            _logger.info(response.status)
            _logger.info(response.data)
            self.sii_xml_response = response.data
            self.sii_result = 'Enviado'

        elif self.company_id.dte_service_provider in ['SII', 'SIIHOMO']:
            print('entró a la alternativa de sii....')
            # 56565656
            # FIRMA Y ENVIA
            # trae los componentes de firma digital
            # aca le incorpora al xml la caratula (de cada uno... cada uno lleva
            # en la caratula un numero de orden del envío.. el cual puede ser
            # en forma simultánea de varios. Se podrían marcar varios
            # documentos sin enviar desde la vista de lista y pulsar el envío
            # todo: ver si es necesario chequear el estado de envio antes de
            # hacerlo, para no enviar dos veces.
            if 1==1:
                signature_d = self.get_digital_signature()
            else:
                raise Warning(_('''There is no Signer Person with an \
authorized signature for you in the system. Please make sure that \
'user_signature_key' module has been installed and enable a digital \
signature, for you or make the signer to authorize you to use his \
signature.'''))
            if 1==1:
                resol_data = self.get_resolution_data(self.company_id)
            else:
                raise Warning(_('''There is no SII Resolution Data \
available for this company. Please go to the company configuration screen and \
set SII resolution data.'''))

            contador_invoice = {}
            for inv in self:
                # para sacar la cantidad de cada una de las invoices
                # recorro el dataset de invoices para determinar las cantidades
                receptor = self.format_vat(inv.partner_id.vat)
                clasedoc = str(inv.sii_document_class_id.sii_code)

                if receptor not in contador_invoice:
                    contador_invoice[receptor] = {}
                    if clasedoc not in contador_invoice[receptor]:
                        contador_invoice[receptor][clasedoc] = []
                if inv.sii_result != 'NoEnviado':
                    continue
                contador_invoice[receptor][clasedoc].append(inv.id)

            # raise Warning(contador_invoice)
            for receptor in contador_invoice:
                print('receptor', receptor)
                caratula = collections.OrderedDict()
                caratula['RutEmisor'] = self.format_vat(inv.company_id.vat)
                caratula['RutEnvia'] = signature_d['subject_serial_number']
                caratula['RutReceptor'] = receptor
                caratula['FchResol'] = resol_data['dte_resolution_date']
                caratula['NroResol'] = resol_data['dte_resolution_number']
                for clasedoc in contador_invoice[receptor]:
                    print('clasedoc', clasedoc, 'cantidad', len(contador_invoice[receptor][clasedoc]))
                    caratula['SubTotDTE'] = collections.OrderedDict()
                    caratula['SubTotDTE']['TpoDTE'] = clasedoc
                    caratula['SubTotDTE']['NroDTE'] = len(contador_invoice[receptor][clasedoc])
                    for invoice in contador_invoice[receptor][clasedoc]:
                        print('id de factura:', invoice)
                        # aca traigo la factura
                        invoice_obj = self.env['account.invoice'].browse(invoice)
                        documento = invoice_obj.sii_xml_request
                        porcion_firma_documento = """\
<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
<SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" /><Reference URI="#MiPE76201224-30158"><Transforms><Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /></Transforms><DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" /><DigestValue>Zi6zVjBT/xgMNdAMmZuOlxdWo7s=</DigestValue></Reference></SignedInfo>
<SignatureValue>{0}</SignatureValue>
<KeyInfo>
<KeyValue>
<RSAKeyValue>
<Modulus>{1}</Modulus>
<Exponent>{2}</Exponent>
</RSAKeyValue>
</KeyValue>
<X509Data>
<X509Certificate>
{3}
</X509Certificate>
</X509Data>
</KeyInfo>
</Signature>"""
                        # ahora firmo
                        print('Documento:')
                        print(documento)
                        print ('Firma:')
                        print(signature_d['priv_key'])
                        frmt = self.signmessage(documento.encode('ascii'), signature_d['priv_key'].encode('ascii'))
                        print('Firmado:')
                        print(frmt)

                        signature = porcion_firma_documento.format(
                            frmt['firma'], frmt['modulus'], frmt['exponent'],
                             signature_d['cert'])



                        print('codificacion documento:', self.whatisthis(documento))
                        print('codificacion firma:', self.whatisthis(signature))

                        invoice_obj.sii_xml_request = """\
<DTE xmlns="http://www.sii.cl/SiiDte" version="1.0">
{}{}
</DTE>""".format(documento, signature)

            #raise Warning('ver....')


#            for inv in self:
#                # ACA se arma la caratula por tipo de comprobante
#                cantidad = contador_invoice[tipodoc]['ctd']
#                # ACA se terminó de arma la caratula por tipo de comprobante
#                # ahora se pasa a iterar las facturas del tipo que está en la caratula
#                for invoices in contador_invoice[tipodoc]['ids']:
#                    invoices
#


#                    # firmante del documento. Aca me tengo que involucrar con el
#                    # objeto del usuario (firma)
#                    # por ahora, firmo con mi propia firma.
#                    # todo: chequear que si no tengo firma, algun usuario del
#                    # sistema me está autorizando.

#
#                    caratd = collections.OrderedDict()
#                    caratd['Caratula'] = caratula
#                    caratxml_pret = etree.tostring(
#                        etree.XML(
#                            dicttoxml.dicttoxml(
#                                caratd, root=False, attr_type=False)),
#                        pretty_print=True) + inv.sii_xml_request
#
#                    # aca seguramente la firma
#                    # primero que nada le quito el tag que está sobre documento
#                    documento = inv.sii_xml_request.replace(
#                        """'<DTE xmlns = "http://www.sii.cl/SiiDte" version = "1.0" >""",
#                        '').replace("""</DTE>""", '')
#                    # ahora firmo
#                    frmt = inv.signmessage(
#                        documento, inv.get_digital_signature()['priv_key'])
#                    print(frmt)
#                    raise Warning(frmt)
#
#
#
#                envelope_efact = '''
#<?xml version="1.0" encoding="ISO-8859-1"?>
#<EnvioDTE xmlns="http://www.sii.cl/SiiDte" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sii.cl/SiiDte EnvioDTE_v10.xsd" version="1.0">
#<SetDTE ID="SDTE151965780">
#{0}</SetDTE>
#<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
#<SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" /><Reference URI="#SDTE151965780"><Transforms><Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" /></Transforms><DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" /><DigestValue>VR8ir9kchZdKtuS/p2I1UN2Q/90=</DigestValue></Reference></SignedInfo>
#<SignatureValue>S+IPqG2jo85+ExxQxIuDCBk/Ju8KpiGsQc9d68p+l0q0hXAP5bAo2ldpDc6seh5sDBWANMhu1Q7PDDpS7rXJXf1X4P2rz4Uoj5zsOZj8lCMt0MKbIdJQ5Vtgp5Du2Nmatb/LwUUycnKcfL+4hZ2AFyRpeHM0TF+LKo30ocOX/e9LIOU0wMQ4e8TS7BcyGmU/NWgoRJ0WkUzdvZqLnsAw1uUHjnTJ5qMCp7K8pqGNaedp5yoQ20IHuf8cihjwtAjfKkbnZGEjLAlBwO31e12n4YQem9zmUhUmI1H+Y2imoIy8FR1azC71S9j5al0jkXcI9x+I3SVF7i+Z6cE8RC3KLw==</SignatureValue>
#<KeyInfo>
#<KeyValue>
#<RSAKeyValue>
#<Modulus>3Qe3t2lICfOYKEPgndrk1SMx7qvhoJrwSdqVpf+VCFHdQlV5FbtLqhbhjH/x5bShROM23NEMh9i8DJAGlxFgmLpHrZEg1emdit1F0yRfVZa0pYw5NTnP8WUEpSHciYyk3cWgwHh7nxNvAYjoVJBrtAmx2iIXpDRyH2TgzGipj3BB5CMkcUHnJZWCyNduqYpp6sGg9KQj5P8iTIroWvi5UNtoU8oSOmkrqhqmBux692nc3jHYxvGCll3aLDdoQN4wrSKXgw0ioCbAX2/nizbToFZ0Sz/HGdlybKwkNviKfQ4DXgAiZ4VE4LiWy8ZY0HKsa9AhhwL5NFSLYF8p+Gn1yw==</Modulus>
#<Exponent>AQAB</Exponent>
#</RSAKeyValue>
#</KeyValue>
#<X509Data>
#<X509Certificate>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</X509Certificate>
#</X509Data>
#</KeyInfo>
#</Signature>
#</EnvioDTE>'''.format(self.convert_encoding(caratxml_pret, 'ISO-8859-1'))
#
#                try:
#                    # realiza la transmisión
#                    # exitosa...
#                    inv.sii_xml_response = response.data
#                    inv.sii_result = 'Enviado'
#                except:
#                    # no pudo hacer el envío
#                    inv.sii_result = 'NoEnviado'

    @api.multi
    def get_xml_file(self):
        return {
            'type' : 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=account.invoice\
&field=sii_xml_request&id=%s&filename=demoxml.xml' % (self.id),
            'target': 'self',
        }

    def get_folio(self, inv):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        # saca el folio directamente de la secuencia
        return inv.journal_document_class_id.sequence_id.number_next_actual

    def get_caf_file(self, inv):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        # hay que buscar el caf correspondiente al comprobante,
        # trayendolo de la secuencia
        returnvalue = False
        #try:
        if 1==1:
            no_caf = True
            caffiles = inv.journal_document_class_id.sequence_id.dte_caf_ids
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            for caffile in caffiles:
                if caffile.status == 'in_use':
                    resultc = base64.b64decode(caffile.caf_file)
                    no_caf = False
                    break
            if no_caf:
                raise Warning(_('''There is no CAF file available or in use \
for this Document. Please enable one.'''))
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            resultcaf = xmltodict.parse(resultc.replace(
                '<?xml version="1.0"?>','',1))

            folio_inicial = resultcaf['AUTORIZACION']['CAF']['DA']['RNG']['D']
            folio_final = resultcaf['AUTORIZACION']['CAF']['DA']['RNG']['H']
            folio = self.get_folio(inv)
            if folio not in range(int(folio_inicial), int(folio_final)):
                msg = '''El folio de este documento: {} está fuera de rango \
del CAF vigente (desde {} hasta {}). Solicite un nuevo CAF en el sitio \
www.sii.cl'''.format(folio, folio_inicial, folio_final)
                _logger.info(msg)
                # defino el status como "spent"
                caffile.status = 'spent'
                raise Warning(_(msg))
            elif folio > int(folio_final) - 2:
                # todo: agregar un wizard al aviso de caf terminándose
                msg = '''El CAF esta pronto a terminarse. Solicite un nuevo \
                CAF para poder continuar emitiendo documentos tributarios'''
            else:
                msg = '''Folio {} OK'''.format(folio)
            _logger.info(msg)
            returnvalue = resultcaf

            #except:
        else:
            pass
        return returnvalue

    def format_vat(self, value):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        return value[2:10] + '-' + value[10:]

    def convert_encoding(self, data, new_coding = 'UTF-8'):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        encoding = cchardet.detect(data)['encoding']
        if new_coding.upper() != encoding.upper():
            data = data.decode(encoding, data).encode(new_coding)
        return data

    def pdf417bc(self, ted):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        bc = barcode(
            'pdf417',
            ted,
            options = dict(
                compact = False,
                eclevel = 5,
                columns = 13,
                rowmult = 2,
                rows = 3
            ),
            margin=20,
            scale=1
        )
        # bc.show()
        # bc.save('test.png')
        return bc

    def digest(self, data):
        sha1 = hashlib.sha1()
        sha1.update(data)
        return sha1.digest()

    def signmessage(self, dd, privkey, pubk=''):
        ddd = self.digest(dd)
        CafPK = M2Crypto.RSA.load_key_string(privkey)
        firma = CafPK.sign(ddd)
        FRMT = base64.b64encode(firma)
        _logger.info(FRMT)
        # agregado nuevo para que no sea necesario mandar la clave publica
        if pubk=='':
            bio = M2Crypto.BIO.MemoryBuffer(privkey)
            rsa = M2Crypto.RSA.load_key_bio(bio)
        else:
            # estas son las dos lineas originales
            bio = M2Crypto.BIO.MemoryBuffer(pubk)
            rsa = M2Crypto.RSA.load_pub_key_bio(bio)
        # fin del cambio
        pubkey = M2Crypto.EVP.PKey()
        pubkey.assign_rsa(rsa)
        # if you need a different digest than the default 'sha1':
        pubkey.reset_context(md='sha1')
        pubkey.verify_init()
        pubkey.verify_update(dd)
        print('verifying....')
        if pubkey.verify_final(firma) == 1:
            print('verified!!!!')
            return {'firma': FRMT, 'modulus': base64.b64encode(rsa.n), 'exponent': base64.b64encode(rsa.e)}

    sii_batch_number = fields.Integer(
        copy=False,
        string='Batch Number',
        readonly=True,
        help='Batch number for processing multiple invoices together'
        )

    sii_barcode = fields.Char(
        copy=False,
        string=_('SII Barcode'),
        readonly=True,
        help='SII Barcode Name'
        )
    sii_barcode_img = fields.Binary(
        copy=False,
        string=_('SII Barcode Image'),
        help='SII Barcode Image in PDF417 format'
        )
    sii_message = fields.Text(
        string='SII Message',
        copy=False,
        )
    sii_xml_request = fields.Text(
        string='SII XML Request',
        copy=False,
        )
    sii_xml_response = fields.Text(
        string='SII XML Response',
        copy=False,
        )
    sii_result = fields.Selection([
        ('', 'n/a'),
        ('NoEnviado', 'No Enviado'),
        ('Enviado', 'Enviado'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
        ('Reparo', 'Reparo'),
        ('Proceso', 'Proceso'),
        ('Reenviar', 'Reenviar'),
        ('Anulado', 'Anulado')],
        'Resultado',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
        help="SII request result",
        default = ''
        )

    @api.multi
    def get_related_invoices_data(self):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        """
        List related invoice information to fill CbtesAsoc.
        """
        self.ensure_one()
        rel_invoices = self.search([
            ('number', '=', self.origin),
            ('state', 'not in',
                ['draft', 'proforma', 'proforma2', 'cancel'])])
        return rel_invoices

    @api.multi
    # def invoice_validate(self):
    def action_number(self):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        self.do_dte_send_invoice()
        res = super(invoice, self).action_number()
        return res

    @api.multi
    def get_barcode(self, dte_service):
        for inv in self:
            ted = False
            folio = self.get_folio(inv)

            result['TED']['DD']['RE'] = inv.format_vat(inv.company_id.vat)
            result['TED']['DD']['TD'] = inv.sii_document_class_id.sii_code
            result['TED']['DD']['F']  = folio
            result['TED']['DD']['FE'] = inv.date_invoice
            result['TED']['DD']['RR'] = inv.format_vat(inv.partner_id.vat)
            result['TED']['DD']['RSR'] = (inv.partner_id.name[:40]).decode(
                'utf-8')
            result['TED']['DD']['MNT'] = int(inv.amount_total)

            for line in inv.invoice_line:
                result['TED']['DD']['IT1'] = line.name.decode('utf-8')
                break

            resultcaf = self.get_caf_file(inv)
            _logger.info(resultcaf)

            result['TED']['DD']['CAF'] = resultcaf['AUTORIZACION']['CAF']
            #_logger.info result
            dte = result['TED']['DD']
            ddxml = '<DD>'+dicttoxml.dicttoxml(
                dte, root=False, attr_type=False).replace(
                '<key name="@version">1.0</key>','',1).replace(
                '><key name="@version">1.0</key>',' version="1.0">',1).replace(
                '><key name="@algoritmo">SHA1withRSA</key>',
                ' algoritmo="SHA1withRSA">').replace(
                '<key name="#text">','').replace(
                '</key>','').replace('<CAF>','<CAF version="1.0">')+'</DD>'
            ###### con esta funcion fuerzo la conversion a iso-8859-1
            ddxml = inv.convert_encoding(ddxml, 'ISO-8859-1')
            # ahora agarro la clave privada y ya tengo los dos elementos
            # que necesito para firmar
            keypriv = (resultcaf['AUTORIZACION']['RSASK']).encode(
                'latin-1').replace('\t','')
            keypub = (resultcaf['AUTORIZACION']['RSAPUBK']).encode(
                'latin-1').replace('\t','')
            #####
            frmt = inv.signmessage(ddxml, keypriv, keypub)['firma']
            ted = (
                '''<TED version="1.0">{}<FRMT algoritmo="SHA1withRSA">{}</FRMT>\
</TED>''').format(ddxml,frmt)
            ted1 = ('{}<FRMT algoritmo="SHA1withRSA">{}</FRMT>').format(
                ddxml,frmt)
            # _logger.info(ted)
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            root = etree.XML(ted)
            # inv.sii_barcode = (etree.tostring(root, pretty__logger.info=True))
            inv.sii_barcode = ted
            image = False
            if ted:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                barcodefile = StringIO()
                image = inv.pdf417bc(ted)
                image.save(barcodefile,'PNG')
                data = barcodefile.getvalue()
                inv.sii_barcode_img = base64.b64encode(data)
        return ted1

    @api.multi
    def do_dte_send_invoice(self):
        cant_doc_batch = 0
        for inv in self.with_context(lang='es_CL'):
            cant_doc_batch = cant_doc_batch + 1
            dte_service = inv.company_id.dte_service_provider
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)

            if dte_service in ['SII', 'SIIHOMO']:
                # debe confeccionar el timbre
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                ted1 = self.get_barcode(dte_service)
            elif dte_service in ['EFACTURADELSUR']:
                # debe utilizar usuario y contraseña
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                dte_usuario = 'nueva.gestion' # eFacturaDelSur
                dte_passwrd = 'e7c1c19cbe' # eFacturaDelSur

                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
            elif dte_service in ['', 'NONE']:
                return

            # definicion de los giros del emisor
            giros_emisor = []
            for turn in inv.company_id.company_activities_ids:
                giros_emisor.extend([{'Acteco': turn.code}])

            # definicion de lineas
            line_number = 1
            invoice_lines = []
            for line in inv.invoice_line:
                lines = collections.OrderedDict()
                lines['NroLinDet'] = line_number
                if line.product_id.default_code:
                    lines['CdgItem'] = collections.OrderedDict()
                    lines['CdgItem']['TpoCodigo'] = 'INT1'
                    lines['CdgItem']['VlrCodigo'] = line.product_id.default_code
                lines['NmbItem'] = line.name
                lines['QtyItem'] = int(round(line.quantity, 0))
                lines['PrcItem'] = int(round(line.price_unit, 0))
                # lines['UnmdItem'] = line.uos_id.name[:4]
                # lines['UnmdItem'] = 'unid'
                if line.discount != 0:
                    lines['DscItem'] = int(round(line.discount, 0))
                lines['MontoItem'] = int(round(line.price_subtotal, 0))
                line_number = line_number + 1
                invoice_lines.extend([{'Detalle': lines}])

            # _logger.info(invoice_lines)
            #########################
            folio = self.get_folio(inv)
            dte = collections.OrderedDict()
            dte1 = collections.OrderedDict()

            # dte['Documento ID'] = 'F{}T{}'.format(folio, inv.sii_document_class_id.sii_code)
            dte['Encabezado'] = collections.OrderedDict()
            dte['Encabezado']['IdDoc'] = collections.OrderedDict()
            dte['Encabezado']['IdDoc']['TipoDTE'] = inv.sii_document_class_id.sii_code
            dte['Encabezado']['IdDoc']['Folio'] = folio
            dte['Encabezado']['IdDoc']['FchEmis'] = inv.date_invoice
            dte['Encabezado']['IdDoc']['FmaPago'] = inv.payment_term.dte_sii_code
            dte['Encabezado']['IdDoc']['FchVenc'] = inv.date_due
            dte['Encabezado']['Emisor'] = collections.OrderedDict()
            dte['Encabezado']['Emisor']['RUTEmisor'] = self.format_vat(
                inv.company_id.vat)
            dte['Encabezado']['Emisor']['RznSoc'] = inv.company_id.name
            dte['Encabezado']['Emisor']['GiroEmis'] = inv.turn_issuer.name[:80]
            dte['Encabezado']['Emisor']['Telefono'] = inv.company_id.phone or ''
            dte['Encabezado']['Emisor']['CorreoEmisor'] = inv.company_id.dte_email
            dte['Encabezado']['Emisor']['item'] = giros_emisor # giros de la compañia - codigos
            dte['Encabezado']['Emisor']['DirOrigen'] = inv.company_id.street
            dte['Encabezado']['Emisor']['CmnaOrigen'] = inv.company_id.state_id.name
            dte['Encabezado']['Emisor']['CiudadOrigen'] = inv.company_id.city
            dte['Encabezado']['Receptor'] = collections.OrderedDict()
            dte['Encabezado']['Receptor']['RUTRecep'] = self.format_vat(
                inv.partner_id.vat)
            dte['Encabezado']['Receptor']['RznSocRecep'] = inv.partner_id.name
            dte['Encabezado']['Receptor']['GiroRecep'] = inv.invoice_turn.name[:40]
            dte['Encabezado']['Receptor']['DirRecep'] = inv.partner_id.street
            dte['Encabezado']['Receptor']['CmnaRecep'] = inv.partner_id.state_id.name
            dte['Encabezado']['Receptor']['CiudadRecep'] = inv.partner_id.city
            dte['Encabezado']['Totales'] = collections.OrderedDict()
            dte['Encabezado']['Totales']['MntNeto'] = int(round(
                inv.amount_untaxed, 0))
            dte['Encabezado']['Totales']['TasaIVA'] = int(round(
                (inv.amount_total / inv.amount_untaxed -1) * 100, 0))
            dte['Encabezado']['Totales']['IVA'] = int(round(inv.amount_tax, 0))
            dte['Encabezado']['Totales']['MntTotal'] = int(round(
                inv.amount_total, 0))
            dte['item'] = invoice_lines
            doc_id = '<Documento ID="F{}T{}">'.format(
                folio, inv.sii_document_class_id.sii_code)
            # si es sii, inserto el timbre
            if dte_service in ['SII', 'SIIHOMO']:
                # inserto el timbre
                dte['TED'] = 'TEDTEDTED'
                # aca completar el XML

            dte1['Documento ID'] = dte
            # xml = dicttoxml.dicttoxml(
            #     dte1, attr_type=False,
            #     custom_root='DTE xmlns="http://www.sii.cl/SiiDte" version="1.0"').replace(
            #     '</DTE xmlns="http://www.sii.cl/SiiDte" version="1.0">', '</DTE>').replace(
            #     '<item>','').replace('</item>','')
            xml = dicttoxml.dicttoxml(
                dte1, root=False, attr_type=False).replace(
                    '<item>','').replace('</item>','')
            # agrego el timbre en caso que sea para el SII
            if dte_service in ['SII', 'SIIHOMO']:
                xml = xml.replace('TEDTEDTED', ted1)

            root = etree.XML( xml )
            xml_pret = (etree.tostring(root, pretty_print=True)).replace(
                    '<Documento_ID>', doc_id).replace(
                    '</Documento_ID>', '</Documento>')
            # _logger.info(xml_pret)
            # en xml_pret está el xml que me interesa
            if dte_service in ['SII', 'SIIHOMO']:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                # lo dejo con format, para ver si es necesario agregar algo más
                # al renderizado.
                envelope_efact = '''{}'''.format(self.convert_encoding(xml_pret, 'ISO-8859-1'))
                inv.sii_xml_request = envelope_efact
                inv.sii_result = 'NoEnviado'

            elif dte_service == 'EFACTURADELSUR':
                # armado del envolvente rrespondiente a EACTURADELSUR

                envelope_efact = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
<soap12:Body>
<PonerDTE xmlns="https://www.efacturadelsur.cl">
<usuario>{}</usuario>
<contrasena>{}</contrasena>
<xml><![CDATA[{}]]></xml>
<enviar>false</enviar>
</PonerDTE>
</soap12:Body>
</soap12:Envelope>'''.format(dte_usuario, dte_passwrd, xml_pret)
                inv.sii_xml_request = envelope_efact
                inv.sii_result = 'NoEnviado'

            elif dte_service == 'FACTURACION':
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                envelope_efact = '''<?xml version="1.0" encoding="ISO-8859-1"?>
{}'''.format(self.convert_encoding(xml_pret, 'ISO-8859-1'))
                inv.sii_xml_request = envelope_efact
                self.get_xml_file()

            elif dte_service == 'ENTERNET':
                # servicio a realizar mediante sponsor
                pass

            elif dte_service == 'FACTURAENLINEA':
                # servicio a realizar mediante sponsor
                pass

            elif dte_service == 'LIBREDTE':
                # servicio a realizar mediante sponsor
                pass

            # en caso que no sea DTE, el proceso es finalizado sin
            # consecuencias (llamando a super
            else:
                _logger.info('NO HUBO NINGUNA OPCION DTE VALIDA')
