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

    @api.multi
    def send_xml_file(self):
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
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        sha1 = hashlib.sha1()
        sha1.update(data)
        return sha1.digest()

    def signmessage(self, dd, privkey, pubk):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        ddd = self.digest(dd)
        CafPK = M2Crypto.RSA.load_key_string(privkey)
        firma = CafPK.sign(ddd)
        FRMT = base64.b64encode(firma)
        _logger.info(FRMT)
        bio = M2Crypto.BIO.MemoryBuffer(pubk)
        rsa = M2Crypto.RSA.load_pub_key_bio(bio)
        pubkey = M2Crypto.EVP.PKey()
        pubkey.assign_rsa(rsa)
        # if you need a different digest than the default 'sha1':
        pubkey.reset_context(md='sha1')
        pubkey.verify_init()
        pubkey.verify_update(dd)
        if pubkey.verify_final(firma) == 1:
            return FRMT

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
            frmt = inv.signmessage(ddxml, keypriv, keypub)
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
                image = inv.pdf417bc(ted)
                image.save('barcode.png')
                with open('barcode.png', 'r') as myfile:
                    data=myfile.read()

                inv.sii_barcode_img = base64.b64encode(data)
        return ted1

    @api.multi
    def do_dte_send_invoice(self):
        for inv in self.with_context(lang='es_CL'):
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

            dte1['Documento ID'] = dte
            xml = dicttoxml.dicttoxml(
                dte1, attr_type=False,
                custom_root='DTE xmlns="http://www.sii.cl/SiiDte" version="1.0"').replace(
                '</DTE xmlns="http://www.sii.cl/SiiDte" version="1.0">', '</DTE>').replace(
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
                envelope_efact = '''<?xml version="1.0" encoding="ISO-8859-1"?>
{}'''.format(self.convert_encoding(xml_pret, 'ISO-8859-1'))
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
                pass

            elif dte_service == 'FACTURAENLINEA':
                pass

            # en caso que no sea DTE, el proceso es finalizado sin
            # consecuencias (llamando a super
            else:
                _logger.info('NO HUBO NINGUNA OPCION DTE VALIDA')
