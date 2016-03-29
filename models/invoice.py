# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
# from pyi25 import PyI25
from openerp import fields, models, api, _
from openerp.exceptions import Warning
import logging
import sys
import traceback
import datetime
import lxml.etree as etree
import collections

from inspect import currentframe, getframeinfo
# estas 2 lineas son para imprimir el numero de linea del script
# (solo para debug)

_logger = logging.getLogger(__name__)

try:
    import xmltodict
except ImportError:
    _logger.debug('Cannot import xmltodict library')

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

# timbre patrón. Permite parsear y formar la tupla patrón corespondiente al documento
timbre  = """<TED version="1.0"><DD><RE>99999999-9</RE><TD>11</TD><F>1</F><FE>2000-01-01</FE><RR>99999999-9</RR><RSR>XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX</RSR><MNT>10000</MNT><IT1>IIIIIII</IT1><CAF version="1.0"><DA><RE>99999999-9</RE><RS>YYYYYYYYYYYYYYY</RS><TD>10</TD><RNG><D>1</D><H>1000</H></RNG><FA>2000-01-01</FA><RSAPK><M>DJKFFDJKJKDJFKDJFKDJFKDJKDnbUNTAi2IaDdtAndm2p5udoqFiw==</M><E>Aw==</E></RSAPK><IDK>300</IDK></DA><FRMA algoritmo="SHA1withRSA">J1u5/1VbPF6ASXkKoMOF0Bb9EYGVzQ1AMawDNOy0xSuAMpkyQe3yoGFthdKVK4JaypQ/F8afeqWjiRVMvV4+s4Q==</FRMA></CAF><TSTED>2014-04-24T12:02:20</TSTED></DD><FRMT algoritmo="SHA1withRSA">jiuOQHXXcuwdpj8c510EZrCCw+pfTVGTT7obWm/fHlAa7j08Xff95Yb2zg31sJt6lMjSKdOK+PQp25clZuECig==</FRMT></TED>"""
result = xmltodict.parse(timbre)
# result es un OrderedDict patrón
# hardcodeamos este valor por ahora


class invoice(models.Model):
    _inherit = "account.invoice"

    def get_folio(self, inv):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        # saca el folio directamente de la secuencia
        return inv.journal_document_class_id.sequence_id.number_next_actual

    def get_caf_file(self):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        # hay que buscar el caf correspondiente al comprobante,
        # trayendolo de la secuencia
        caffile = self.journal_document_class_id.sequence_id.caf_file
        resultcaf = xmltodict.parse(
            base64.b64decode(caffile).replace(
                '<?xml version="1.0"?>','',1))['AUTORIZACION']['CAF']['DA']
        return resultcaf

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
        bc.show()
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
        print(FRMT)
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

    sii_caf = fields.Char(
        copy=False,
        string='CAF Stamp',
        readonly=True,
        help='CAF Stamp XML File'
        )

    sii_barcode = fields.Char(
        compute='_get_barcode',
        string=_('SII Barcode'),
        help='SII Barcode Name'
        )
    sii_barcode_img = fields.Binary(
        compute='_get_barcode',
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
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
        ('Reparo', 'Reparo'),
        ('Enviado', 'Enviado'),
        ('Proceso', 'Proceso'),
        ('Reenviar', 'Reenviar'),
        ('NoEnviado', 'NoEnviado'),
        ('Anulado', 'Anulado')],
        'Resultado',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
        help="SII request result"
        )

    @api.one
    @api.depends('sii_caf')
    def _get_barcode(self):
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        ted = False
        if self.sii_caf:
            # si no hay CAF saltea toda esta parte
            # hardcodeo de datos a usar en el ensamblado del timbre.
            # luego serán entregados por objetos de Odoo

            # aca trae las lineas de la factura, pero para el timbre
            # con la primer linea le alcanza.
            account_invoice_line_fields = [
                {'name':'Servicio de Instalación de Cables','nn':99999},
                {'name':'Llevarle el paquete','nn':99999},
            ]
            result['TED']['DD']['RE'] = self.format_vat(self.company_id.vat)
            result['TED']['DD']['TD'] = self.sii_document_class_id.sii_code
            result['TED']['DD']['F']  = self.get_document_number()
            result['TED']['DD']['FE'] = self.date_invoice
            result['TED']['DD']['RR'] = self.format_vat(self.partner_id.vat)
            result['TED']['DD']['RSR'] = (self.partner_id.name[:40]).decode('utf-8')
            result['TED']['DD']['MNT'] = self.amount_total
            # solo toma la primer linea en el timbre
            for line in account_invoice_line_fields:
                result['TED']['DD']['IT1'] = (line['name']).decode('utf-8')
                break

            resultcaf = self.get_caf_file()

            result['TED']['DD']['CAF'] = resultcaf['AUTORIZACION']['CAF']
            #print result
            dte = result['TED']['DD']
            ddxml = '<DD>'+dicttoxml.dicttoxml(dte, root=False, attr_type=False).replace('<key name="@version">1.0</key>','',1).replace('><key name="@version">1.0</key>',' version="1.0">',1).replace('><key name="@algoritmo">SHA1withRSA</key>',' algoritmo="SHA1withRSA">').replace('<key name="#text">','').replace('</key>','')+'</DD>'
            ###### con esta funcion fuerzo la conversion a iso-8859-1
            ddxml = self.convert_encoding(ddxml, 'ISO-8859-1')
            #ahora agarro la clave privada y ya tengo los dos elementos que necesito para firmar
            keypriv = (resultcaf['AUTORIZACION']['RSASK']).encode('latin-1').replace('\t','')
            keypub = (resultcaf['AUTORIZACION']['RSAPUBK']).encode('latin-1').replace('\t','')
            #####
            frmt = self.signmessage(ddxml, keypriv, keypub)
            ted = ('<TED version="1.0">{}<FRMT algoritmo="SHA1withRSA">{}</FRMT></TED>').format(ddxml,frmt)

            print(ted)
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            self.sii_barcode = ted

            image = False
            if ted:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                image = self.pdf417bc(ted)
                image.save('/l10n_cl_dte_wsii/bcode.png')
                # aca open() el archivo y meterlo en la variable
                # igual que se hizo en el control de horarios jacc
                # o usar stringIO como sale acá
                # http://stackoverflow.com/questions/21992520/python-elaphe-barcode-generation-issues
                self.sii_barcode_img = image

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
    def do_dte_send_invoice(self):
        # hardcodeamos la accion provisoriamente
        dte_service = 'EFACTURADELSUR'
        dte_usuario = 'miusuario'
        dte_passwrd = 'micontrasenia'
        frameinfo = getframeinfo(currentframe())
        print(frameinfo.filename, frameinfo.lineno)
        for inv in self.with_context(lang='es_CL'):
            # Ignore invoices with caf
            # apenas valido:
            # si es wssii: (esto lo se, diciendo "si la secuencia del comprobante del diario es DTE (is_dte)")
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            if inv.journal_document_class_id.sequence_id.is_dte:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                # si tiene caf: (esto lo se, diciendo:
                #  "si la secuencia del comprobante del diario tiene un CAF
                # asociado (caf no es null o vacio o none)")
                # agregar también "si el caf que tiene no está vencido"
                if inv.journal_document_class_id.sequence_id.dte_caf_ids:
                    frameinfo = getframeinfo(currentframe())
                    print(frameinfo.filename, frameinfo.lineno)
                    # es buscar el caf a la secuencia
                    # traerlo
                    # crear el timbre
                    # crear el grafico
                    # dejo esta parte para después ya que no es prioritaria por
                    # ahora
                    # Si entró por acá significa que voy a usar SII como servicio
                    dte_service = 'WSSII'
                    pass
                # en caso que no haya CAF asociado, solo confecciona el XML
                # el formato del XML que tiene que armar, depende del servicio
                # de factura electrónica que se esté usando.. puede ser
                # varias opciones... por ahora tenemos varios.....
                # por ahora, van hardcodeados acá pero la idea es hacer un modulo
                # para contener la plantilla txt o xml que pide cada provider.
                ##############################################################
                # XML file is equal for seral services
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)

                # definicion de los giros del emisor
                giros_emisor = []
                for turn in inv.company_id.company_activities_ids:
                    giros_emisor.extend([{'Acteco': turn.code}])
                # ....

                # definicion de las lineas
                line_number = 1
                invoice_lines = []
                for line in inv.invoice_line:
                    lines = collections.OrderedDict()
                    lines['NroLinDet'] = line_number
                    lines['CdgItem'] = collections.OrderedDict()
                    lines['CdgItem']['TpoCodigo'] = 'INT1'
                    lines['CdgItem']['VlrCodigo'] = line.product_id.default_code or ''
                    lines['NmbItem'] = line.name
                    lines['QtyItem'] = int(round(line.quantity, 0))
                    lines['PrcItem'] = int(round(line.price_unit, 0))
                    lines['UnmdItem'] = line.uos_id.name
                    lines['DscItem'] = int(round(line.discount, 0))
                    lines['MontoItem'] = int(round(line.price_subtotal, 0))
                    line_number = line_number + 1
                    invoice_lines.extend([{'Detalle': lines}])

                print(invoice_lines)
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
                dte['Encabezado']['IdDoc']['FmaPago'] = inv.payment_term.name
                dte['Encabezado']['IdDoc']['FchVenc'] = inv.date_due
                dte['Encabezado']['Emisor'] = collections.OrderedDict()
                dte['Encabezado']['Emisor']['RUTEmisor'] = self.format_vat(inv.company_id.vat)
                dte['Encabezado']['Emisor']['RznSoc'] = inv.company_id.name
                dte['Encabezado']['Emisor']['GiroEmis'] = inv.turn_issuer.name
                dte['Encabezado']['Emisor']['Telefono'] = inv.company_id.phone or ''
                dte['Encabezado']['Emisor']['CorreoEmisor'] = inv.company_id.dte_email
                dte['Encabezado']['Emisor']['item'] = giros_emisor # giros de la compañia - codigos
                dte['Encabezado']['Emisor']['DirOrigen'] = inv.company_id.street
                dte['Encabezado']['Emisor']['CmnaOrigen'] = inv.company_id.state_id.name
                dte['Encabezado']['Emisor']['CiudadOrigen'] = inv.company_id.city
                dte['Encabezado']['Receptor'] = collections.OrderedDict()
                dte['Encabezado']['Receptor']['RUTRecep'] = self.format_vat(inv.partner_id.vat)
                dte['Encabezado']['Receptor']['RznSocRecep'] = inv.partner_id.name
                dte['Encabezado']['Receptor']['GiroRecep'] = inv.invoice_turn.name
                dte['Encabezado']['Receptor']['DirRecep'] = inv.partner_id.street
                dte['Encabezado']['Receptor']['CmnaRecep'] = inv.partner_id.state_id.name
                dte['Encabezado']['Receptor']['CiudadRecep'] = inv.partner_id.city
                dte['Encabezado']['Totales'] = collections.OrderedDict()
                dte['Encabezado']['Totales']['MntNeto'] = int(round(inv.amount_untaxed, 0))
                dte['Encabezado']['Totales']['TasaIVA'] = int(round((inv.amount_total / inv.amount_untaxed -1) * 100, 0))
                dte['Encabezado']['Totales']['IVA'] = int(round(inv.amount_tax, 0))
                dte['Encabezado']['Totales']['MntTotal'] = int(round(inv.amount_total, 0))
                dte['item'] = invoice_lines
                doc_id = '<Documento ID="F{}T{}">'.format(folio, inv.sii_document_class_id.sii_code)
                # print(doc_id)
                dte1['Documento ID'] = dte
                ##############################################################
                if dte_service == 'WSSII':
                    frameinfo = getframeinfo(currentframe())
                    print(frameinfo.filename, frameinfo.lineno)
                    pass
                elif dte_service == 'EFACTURADELSUR':
                    # print(dte)

                    xml = dicttoxml.dicttoxml(
                        dte1, attr_type=False,
                        custom_root='DTE xmlns="http://www.sii.cl/SiiDte" version="1.0"').replace(
                            '</DTE xmlns="http://www.sii.cl/SiiDte" version="1.0">', '</DTE>').replace(
                            '<item>','').replace('</item>','')
                    root = etree.XML( xml )
                    xml_pret = (
                        etree.tostring(root, pretty_print=True))
                    # print(xml_pret)   

                    envelope_efact = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
<soap12:Body>
<PonerDTE xmlns="https://www.efacturadelsur.cl">
<usuario>{}</usuario>
<contrasena>{}</contrasena>
<xml>
{}</xml>
<enviar>boolean</enviar>
</PonerDTE>
</soap12:Body>
</soap12:Envelope>'''.format(dte_usuario, dte_passwrd, xml_pret)

                    inv.sii_xml_request = envelope_efact.replace(
                        '<Documento_ID>', doc_id).replace(
                        '</Documento_ID>', '</Documento>')
                    # print(type(inv.sii_xml_request))
                elif dte_service == 'FACTURACION':
                    frameinfo = getframeinfo(currentframe())
                    print(frameinfo.filename, frameinfo.lineno)
                    pass
                elif dte_service == 'ENTERNET':
                    frameinfo = getframeinfo(currentframe())
                    print(frameinfo.filename, frameinfo.lineno)
                    pass
                elif dte_service == 'FACTURAENLINEA':
                    frameinfo = getframeinfo(currentframe())
                    print(frameinfo.filename, frameinfo.lineno)
                    pass
            # en caso que no sea DTE, el proceso es finalizado sin
            # consecuencias (llamando a super
            else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
'''

            if inv.sii_caf:
                continue


            # Ignore invoice if not ws on point of sale
            if not sii_ws:
                continue
            # get the electronic invoice type, point of sale and sii_ws:
            commercial_partner = inv.commercial_partner_id
            country = commercial_partner.country_id
            journal = inv.journal_id
            point_of_sale = journal.point_of_sale_id
            pos_number = point_of_sale.number
            doc_sii_code = self.sii_document_class_id.sii_code
            next_invoice_number = self.get_folio()
            partner_doc_code = commercial_partner.document_type_id.sii_code
            tipo_doc = partner_doc_code or '99'
            nro_doc = partner_doc_code and commercial_partner.document_number.replace('.','') or "0"
            cbt_desde = cbt_hasta = cbte_nro = next_invoice_number
            concepto = tipo_expo = int(inv.invoice_turn)

            fecha_cbte = inv.date_invoice
            # no cumple esta opcion
            fecha_cbte = fecha_cbte.replace("-", "")
            # due and billing dates only for concept "services"
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            if int(concepto) != 1:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                fecha_venc_pago = inv.date_due
                #fecha_serv_desde = inv.sii_service_start
                #fecha_serv_hasta = inv.sii_service_end
                if sii_ws != 'wsmtxca':
                    fecha_venc_pago = fecha_venc_pago.replace("-", "")
                    #fecha_serv_desde = fecha_serv_desde.replace("-", "")
                    #fecha_serv_hasta = fecha_serv_hasta.replace("-", "")
            else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                fecha_venc_pago = fecha_serv_desde = fecha_serv_hasta = None

            # # invoice amount totals:
            imp_total = str("%.2f" % abs(inv.amount_total))
            imp_tot_conc = "0.00"
            imp_neto = str("%.2f" % abs(inv.amount_untaxed))
            imp_iva = str("%.2f" % abs(inv.vat_amount))
            imp_subtotal = imp_neto  # TODO: not allways the case!
            imp_trib = str("%.2f" % abs(inv.other_taxes_amount))
            # imp_op_ex = str("%.2f" % abs(inv.vat_exempt_amount))
            moneda_id = inv.currency_id.sii_code
            # moneda_ctz = inv.currency_rate
            # moneda_ctz = str(inv.company_id.currency_id.compute(
                # 1., inv.currency_id))

            # # foreign trade data: export permit, country code, etc.:
            # if inv.sii_incoterm_id:
            #     incoterms = inv.sii_incoterm_id.sii_code
            #     incoterms_ds = inv.sii_incoterm_id.name
            # else:
            #     incoterms = incoterms_ds = None
            if int(doc_sii_code) in [19, 20, 21] and tipo_expo == 1:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                permiso_existente = "N" or "S"     # not used now
            else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                permiso_existente = ""
            obs_generales = inv.comment
            if inv.payment_term:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                forma_pago = inv.payment_term.name
                obs_comerciales = inv.payment_term.name
            else:
                frameinfo = getframeinfo(currentframe())
                print(frameinfo.filename, frameinfo.lineno)
                forma_pago = obs_comerciales = None
            idioma_cbte = 1     # invoice language: spanish / español
            ## customer data (foreign trade):
            nombre_cliente = commercial_partner.name
            print(nombre_cliente)
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            # If argentinian and cuit, then use cuit
            if country.code == 'AR' and tipo_doc == 80 and nro_doc:
                id_impositivo = nro_doc
                cuit_pais_cliente = None
            # If not argentinian and vat, use vat
            elif country.code != 'AR' and commercial_partner.vat:
                id_impositivo = commercial_partner.vat[2:]
                cuit_pais_cliente = None
            # else use cuit pais cliente
            else:
                id_impositivo = None
                if commercial_partner.is_company:
                    cuit_pais_cliente = country.cuit_juridica
                else:
                    cuit_pais_cliente = country.cuit_fisica

            domicilio_cliente = " - ".join([
                                commercial_partner.name or '',
                                commercial_partner.street or '',
                                commercial_partner.street2 or '',
                                commercial_partner.zip or '',
                                commercial_partner.city or '',
                                ])
            # pais_dst_cmp = commercial_partner.country_id.sii_code

            # create the invoice internally in the helper
            if sii_ws:
                ws.CrearFactura(
                    concepto, tipo_doc, nro_doc, doc_sii_code, pos_number,
                    cbt_desde, cbt_hasta, imp_total, imp_tot_conc, imp_neto,
                    imp_iva,
                    imp_trib, imp_op_ex, fecha_cbte, fecha_venc_pago,
                    fecha_serv_desde, fecha_serv_hasta,
                    moneda_id, moneda_ctz
                )
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            # TODO ver si en realidad tenemos que usar un vat pero no lo
            # subimos
            CbteAsoc = inv.get_related_invoices_data()
            if CbteAsoc:
                ws.AgregarCmpAsoc(
                    CbteAsoc.sii_document_class_id.sii_code,
                    CbteAsoc.point_of_sale,
                    CbteAsoc.invoice_number,
                    )

            # analize line items - invoice detail
            # wsfe do not require detail
            vto = None
            msg = False
            frameinfo = getframeinfo(currentframe())
            print(frameinfo.filename, frameinfo.lineno)
            try:
                if sii_ws:
                    ws.CAESolicitar()
                    vto = ws.Vencimiento
            except SoapFault as fault:
                msg = 'Falla SOAP %s: %s' % (
                    fault.faultcode, fault.faultstring)
            except Exception, e:
                msg = e
            except Exception:
                if ws.Excepcion:
                    # get the exception already parsed by the helper
                    msg = ws.Excepcion
                else:
                    # avoid encoding problem when raising error
                    msg = traceback.format_exception_only(
                        sys.exc_type,
                        sys.exc_value)[0]
            if msg:
                raise Warning(_('SII Validation Error. %s' % msg))

            # msg = u"\n".join([ws.Obs or "", ws.ErrMsg or ""])
            # if not ws.CAE or ws.Resultado != 'A':
            #     raise Warning(_('SII Validation Error. %s' % msg))
            # TODO ver que algunso campos no tienen sentido porque solo se
            # escribe aca si no hay errores
            '''
#### CODIGO DE PRUEBA #####

#from signsharsa import i
#i = i()

# esta biblioteca sirve para detectar encoding y cambiarla
# util para codificar en ISO-8859-1

frameinfo = getframeinfo(currentframe())
print(frameinfo.filename, frameinfo.lineno)

'''
caffile = """
<?xml version="1.0"?>
<AUTORIZACION>
	<CAF version="1.0">
		<DA>
			<RE>76201224-3</RE>
			<RS>SOCIEDAD DE SERVICIOS HECTOR DANIEL BLAN</RS>
			<TD>34</TD>
			<RNG><D>1</D><H>20</H></RNG>
			<FA>2014-01-20</FA>
			<RSAPK><M>yDShk1KFeS0P7M12l6mpYMRy2LalYnMR+VEdnvGjy19xFOeOEgTwNXZaajAtaJfwFrkPoOV9sYacgnsmiuqosQ==</M><E>Aw==</E></RSAPK>
			<IDK>100</IDK>
		</DA>
		<FRMA algoritmo="SHA1withRSA">
			s4ivozzep5Mc+aSyVjJZ6smouuak2WDZc6uXFTs4OHf2cx3y+nwzjBp6x4Pj3oHrRY5xC7O9iZYGtNUTvslseg==
		</FRMA>
	</CAF>
	<RSASK>-----BEGIN RSA PRIVATE KEY-----
	MIIBOgIBAAJBAMg0oZNShXktD+zNdpepqWDEcti2pWJzEflRHZ7xo8tfcRTnjhIE
	8DV2WmowLWiX8Ba5D6DlfbGGnIJ7JorqqLECAQMCQQCFeGu3jFj7c1/zM6RlG8ZA
	gvc7JG5Bogv7i2kUoRfc6R0kF+os36AuBlA1oZErKtv2ymXxojnvppXq39tWyHmj
	AiEA7j07wcaUNZrEwJy+YaXnaypCeBf5EfHsq2DTWi+SgcMCIQDXIYftCCFKVagh
	fP9yAfA6+kb+nnkU2CAQQVgDWStwewIhAJ7TfSvZuCO8gysTKZZumkdxgaVlULah
	SHJAjObKYavXAiEAj2uv81rA3DkawP3/oVagJ1GEqb77YzrACtY6rOYc9acCIFhI
	akF8695xmqziO+I25nLcn0lf2mRdCe9IvdNxvaH+
	-----END RSA PRIVATE KEY-----
	</RSASK>
	<RSAPUBK>-----BEGIN PUBLIC KEY-----
	MFowDQYJKoZIhvcNAQEBBQADSQAwRgJBAMg0oZNShXktD+zNdpepqWDEcti2pWJz
	EflRHZ7xo8tfcRTnjhIE8DV2WmowLWiX8Ba5D6DlfbGGnIJ7JorqqLECAQM=
	-----END PUBLIC KEY-----
	</RSAPUBK>
</AUTORIZACION>
""".replace('<?xml version="1.0"?>','',1)

#print result['TED']['DD']
'''