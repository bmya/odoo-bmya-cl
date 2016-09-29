# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _
from openerp.exceptions import Warning as UserError
import logging, json
import lxml.etree as etree
from lxml import objectify
from lxml.etree import XMLSyntaxError

import collections, re

import urllib3, certifi, xmltodict, dicttoxml, base64, cchardet, os

urllib3.disable_warnings()
'''
pip install --upgrade requests
y
pip install --upgrade urllib3
'''

pool = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)
_logger = logging.getLogger(__name__)

# hardcodeamos este valor por ahora
xsdpath = os.path.dirname(os.path.realpath(__file__)).replace(
    '/models','/static/xsd/')
host = 'https://libredte.cl/api'
api_emitir = host + '/dte/documentos/emitir'
api_generar = host + '/dte/documentos/generar'
api_gen_pdf = host + '/dte/documentos/generar_pdf'
api_upd_satus = host + '/dte/dte_emitidos/actualizar_estado/'
no_product = False
special_chars = [
    [u'á', 'a'],
    [u'é', 'e'],
    [u'í', 'i'],
    [u'ó', 'o'],
    [u'ú', 'u'],
    [u'ñ', 'n'],
    [u'Á', 'A'],
    [u'É', 'E'],
    [u'Í', 'I'],
    [u'Ó', 'O'],
    [u'Ú', 'U'],
    [u'Ñ', 'N']
]

class invoice(models.Model):
    '''
    Extensión del modelo de datos para contener parámetros globales necesarios
    para todas las integraciones de factura electrónica.
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2016-06-11
    '''

    _inherit = "account.invoice"

    def char_replace(self, text):
        """
        Funcion para reemplazar caracteres especiales
        Esta funcion sirve para salvar bug en libreDTE con los recortes de
        giros que están codificados en utf8 (cuando trunca, trunca la
        codificacion)
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-07-31
        """
        for char in special_chars:
            try:
                text = text.replace(char[0], char[1])
            except:
                pass
        print(text)
        return text

    def create_template_doc(self, doc):
        """
        Creacion de plantilla xml para envolver el DTE
        Previo a realizar su firma (1)
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-01
        """
        xml = '''<DTE xmlns="http://www.sii.cl/SiiDte" version="1.0">
<!-- Odoo Implementation Blanco Martin -->
{}</DTE>'''.format(doc)
        return xml

    def create_template_envio(self, RutEmisor, RutReceptor, FchResol, NroResol,
                              TmstFirmaEnv, TpoDTE, EnvioDTE):
        """
        Funcion que permite crear una plantilla para el EnvioDTE
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-01
        """
        signature_d = self.get_digital_signature_pem(self.company_id)

        xml = '''<SetDTE ID="OdooBMyA">
<Caratula version="1.0">
<RutEmisor>{0}</RutEmisor>
<RutEnvia>{1}</RutEnvia>
<RutReceptor>{2}</RutReceptor>
<FchResol>{3}</FchResol>
<NroResol>{4}</NroResol>
<TmstFirmaEnv>{5}</TmstFirmaEnv>
<SubTotDTE>
<TpoDTE>{6}</TpoDTE>
<NroDTE>1</NroDTE>
</SubTotDTE>
</Caratula>
{7}
</SetDTE>
'''.format(RutEmisor, signature_d['subject_serial_number'], RutReceptor,
           FchResol, NroResol, TmstFirmaEnv, TpoDTE, EnvioDTE)
        return xml

    def remove_indents(self, xml):
        """
        Funcion para remover los indents del documento previo a enviar el xml
        a firmaar. Realizada para probar si el problema de
        error de firma proviene de los indents.
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-01
        """
        return xml.replace(
            '        <', '<').replace(
            '      <', '<').replace(
            '    <', '<').replace(
            '  <', '<')

    def convert_encoding(self, data, new_coding='UTF-8'):
        """
        Funcion auxiliar para conversion de codificacion de strings
        proyecto experimentos_dte
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2014-12-01
        """
        encoding = cchardet.detect(data)['encoding']
        if new_coding.upper() != encoding.upper():
            data = data.decode(encoding, data).encode(new_coding)
        return data

    def whatisthis(self, s):
        """
        Funcion auxiliar para saber que codificacion tiene el string
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-01
        """
        if isinstance(s, str):
            _logger.info("ordinary string")
        elif isinstance(s, unicode):
            _logger.info("unicode string")
        else:
            _logger.info("not a string")

    def create_headers_ldte(self, comp_id=False):
        """
        Función para crear los headers necesarios por LibreDTE
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-23
        """
        if comp_id:
            dte_username = comp_id.dte_username
            dte_password = comp_id.dte_password
        else:
            dte_username = self.company_id.dte_username
            dte_password = self.company_id.dte_password
        headers = {}
        headers['Authorization'] = 'Basic {}'.format(
            base64.b64encode('{}:{}'.format(
                dte_password, dte_username)))
        headers['Accept-Encoding'] = 'gzip, deflate, identity'
        headers['Accept'] = '*/*'
        headers['User-Agent'] = 'python-requests/2.6.0 CPython/2.7.6 \
Linux/3.13.0-88-generic'
        headers['Connection'] = 'keep-alive'
        headers['Content-Type'] = 'application/json'
        return headers


    def xml_validator(self, some_xml_string, validacion='doc'):
        """
        Funcion para validar los xml generados contra el esquema que le
        corresponda segun el tipo de documento.
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-01
        """
        if 1==1:
            validacion_type = {
                'doc': 'DTE_v10.xsd',
                'env': 'EnvioDTE_v10.xsd',
                'sig': 'xmldsignature_v10.xsd'
            }
            xsd_file = xsdpath+validacion_type[validacion]
            try:
                schema = etree.XMLSchema(file=xsd_file)
                parser = objectify.makeparser(schema=schema)
                objectify.fromstring(some_xml_string, parser)
                _logger.info(_("The Document XML file validated correctly: \
(%s)") % validacion)
                return True
            except XMLSyntaxError as e:
                _logger.info(_("The Document XML file has error: %s") % e.args)
                raise UserError(_('XML Malformed Error %s') % e.args)

    @api.multi
    def check_dte_status(self):
        """
        obtener estado de DTE.
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-16
        """
        self.ensure_one()
        folio = self.get_folio_current()
        if self.dte_service_provider in [
            'EFACTURADELSUR', 'EFACTURADELSUR_TEST']:
            # reobtener el folio
            folio = self.get_folio_current(self.document_number)
            dte_username = self.company_id.dte_username
            dte_password = self.company_id.dte_password
            envio_check = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <ObtenerEstadoDTE xmlns="https://www.efacturadelsur.cl">
      <usuario>{0}</usuario>
      <contrasena>{1}</contrasena>
      <rutEmisor>{2}</rutEmisor>
      <tipoDte>{3}</tipoDte>
      <folio>{4}</folio>
    </ObtenerEstadoDTE>
  </soap12:Body>
</soap12:Envelope>'''.format(
            dte_username,
            dte_password,
            self.format_vat(self.company_id.vat),
            self.sii_document_class_id.sii_code,
            folio)

            _logger.info("envio: %s" % envio_check)
            host = 'https://www.efacturadelsur.cl'
            post = '/ws/DTE.asmx'  # HTTP/1.1
            url = host + post
            _logger.info('URL to be used %s' % url)
            response = pool.urlopen('POST', url, headers={
                'Content-Type': 'application/soap+xml',
                'charset': 'utf-8',
                'Content-Length': len(
                    envio_check)}, body=envio_check)
            _logger.info(response.status)
            _logger.info(response.data)
            if response.status != 200:
                pass
                raise UserError(
                    'The Transmission Has Failed. Error: %s' % response.status)

            setenvio = {
                # 'sii_result': 'Enviado' if self.dte_service_provider ==
                # 'EFACTURADELSUR' else self.sii_result,
                'sii_xml_response1': response.data}
            self.write(setenvio)
            x = xmltodict.parse(response.data)
            raise UserError(x['soap:Envelope']['soap:Body'][
                              'ObtenerEstadoDTEResponse'][
                              'ObtenerEstadoDTEResult'])

            root = etree.fromstring(response.data)
            raise UserError(root.ObtenerEstadoDTEResult)

        elif self.dte_service_provider in [
            'LIBREDTE', 'LIBREDTE_TEST']:
            '''
            {
                "track_id": ---,
                "revision_estado": "EPR - Envio Procesado",
                "revision_detalle": "DTE aceptado"
            }
            '''
            headers = self.create_headers_ldte()
            metodo = 1  # =1 servicio web, =0 correo
            # consultar estado de dte emitido
            response_status = pool.urlopen(
                'GET',
                api_upd_satus + str(
                    self.sii_document_class_id.sii_code) + '/' + str(
                    folio) + '/' + str(self.format_vat(
                    self.company_id.vat)) + '/' + str(metodo),
                headers=headers)

            if response_status.status != 200:
                raise UserError(
                    'Error al obtener el estado del DTE emitido: {}'.format(
                        response_status.data))
            _logger.info('Se recibió una respuesta:')
            _logger.info(response_status.data)
            response_status_j = json.loads(response_status.data)
            _logger.info(response_status_j['track_id'])
            _logger.info(response_status_j['revision_estado'])
            _logger.info(response_status_j['revision_detalle'])
            if response_status_j['revision_estado'] in [
                'DTE aceptado', 'RLV - DTE Aceptado con Reparos Leves'] or \
                response_status_j['revision_detalle'] == 'DTE aceptado':
                resultado_status = 'Aceptado'
            elif response_status_j['revision_estado'] == '-11':
                raise UserError('Atención: Revisión en Proceso')
            elif response_status_j['revision_estado'] in [
                'RCH - DTE Rechazado', 'RFR - Rechazado por Error en Firma']:
                resultado_status = 'Rechazado'
            else:
                resultado_status = self.sii_result
            _logger.info('a grabar resultado_status: {}'.format(
                resultado_status))
            setenvio = {
                'sii_xml_response2': response_status.data,
                'sii_result': resultado_status,
                'invoice_printed': 'printed'
            }
            self.write(setenvio)
            _logger.info(
                'resultado_status grabado: {}'.format(self.sii_result))
            _logger.info(response_status_j['revision_estado'])


    @api.multi
    def send_dte(self):
        """
        Realización del envío de DTE.
        nota: se cambia el nombre de la función de "send xml file"
        a "send_dte" para ser mas abarcativa en cuanto a que algunos
        service provider no trabajan con xml sino con un diccionario
        (caso de libre dte por ejemplo). Como la funcion se invoca desde un
        boton, pero trambién se podría cambiar aejecutar automaticamente,
        pienso que es más conveniente tratar todas las opciones de provider
        en la misma funcion.
        La funcion selecciona el proveedor de servicio de DTE y efectua el envio
        de acuerdo a la integracion del proveedor.
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-01
        """
        self.ensure_one()

        _logger.info('Entering Send XML Function')
        _logger.info(
            'Service provider is: %s' % self.dte_service_provider)

        if self.dte_service_provider in [
            'EFACTURADELSUR', 'EFACTURADELSUR_TEST']:
            host = 'https://www.efacturadelsur.cl'
            post = '/ws/DTE.asmx' # HTTP/1.1
            url = host + post
            _logger.info('URL to be used %s' % url)
            _logger.info('Lenght used for forming envelope: %s' % len(
                self.sii_xml_request))
            response = pool.urlopen('POST', url, headers={
                'Content-Type': 'application/soap+xml',
                'charset': 'utf-8',
                'Content-Length': len(
                    self.sii_xml_request)}, body=self.sii_xml_request)
            _logger.info(response.status)
            _logger.info(response.data)
            if response.status != 200:
                raise UserError(
                    'The Transmission Has Failed. Error: %s' % response.status)
            setenvio = {
                'sii_result': 'Enviado' \
                    if self.dte_service_provider == 'EFACTURADELSUR' \
                    else self.sii_result,
                'sii_xml_response1': response.data}
            self.write(setenvio)

        elif self.dte_service_provider in ['LIBREDTE', 'LIBREDTE_TEST']:
            '''
            LibreDTE no necesita enviar el DTE desde nuestra app. envia solo
            el diccionario.
            '''
            pass
        else:
            pass

    @api.multi
    def get_xml_file(self):
        """
        Funcion para descargar el xml en el sistema local del usuario
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-05-01
        """
        return {
            'type' : 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=account.invoice\
&field=sii_xml_request&id=%s&filename=demoxml.xml' % (self.id),
            'target': 'self',
        }

    def get_folio(self, inv):
        """
        Funcion para descargar el folio tomando el valor desde la secuencia
        correspondiente al tipo de documento.
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-05-01
        """
        # saca el folio directamente de la secuencia
        return inv.journal_document_class_id.sequence_id.number_next_actual

    def set_folio(self, inv, folio):
        """
        Funcion para actualizar el folio tomando el valor devuelto por el
        tercera parte integrador.
        Esta funcion se usa cuando un tercero comanda los folios
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-23
        """
        inv.journal_document_class_id.sequence_id.number_next_actual = folio

    def get_company_dte_service_provider(self):
        """
        Funcion que devuelve el service provider desde la compañia
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-05-01
        """
        # raise UserError(self.company_id.dte_service_provider)
        return self.company_id.dte_service_provider

    def get_folio_current(self):
        """
        Funcion para obtener el folio ya registrado en el dato
        correspondiente al tipo de documento.
        (remoción del prefijo almacenado)
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-05-01
        """
        prefix = self.journal_document_class_id.sequence_id.prefix
        try:
            folio = self.sii_document_number.replace(prefix, '', 1)
        except:
            folio = self.sii_document_number
        return int(folio)

    def format_vat(self, value):
        return value[2:10] + '-' + value[10:]


    """
    Definicion de extension de modelo de datos para account.invoice
    @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
    @version: 2015-02-01
    """
    sii_batch_number = fields.Integer(
        copy=False,
        string='Batch Number',
        readonly=True,
        help='Batch number for processing multiple invoices together')

    sii_barcode = fields.Char(
        copy=False,
        string=_('SII Barcode'),
        readonly=True,
        help='SII Barcode Name')

    sii_barcode_img = fields.Binary(
        copy=False,
        string=_('SII Barcode Image'),
        readonly=True,
        help='SII Barcode Image in PDF417 format')

    sii_message = fields.Text(
        string='SII Message',
        readonly=True,
        copy=False)
    sii_xml_request = fields.Text(
        string='XML Request',
        readonly=True,
        copy=False)
    sii_xml_response1 = fields.Text(
        string='XML Response 1',
        readonly=True,
        copy=False)
    sii_xml_response2 = fields.Text(
        string='XML Response 2',
        readonly=True,
        copy=False)
    sii_send_ident = fields.Text(
        string='SII Send Identification',
        readonly=False,
        copy=False)
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
        default = '')

    dte_service_provider = fields.Selection(
        (
            ('', 'None'),
            ('EFACTURADELSUR', 'efacturadelsur.cl'),
            ('EFACTURADELSUR_TEST', 'efacturadelsur.cl (test mode)'),
            ('ENTERNET', 'enternet.cl'),
            ('FACTURACION', 'facturacion.cl'),
            ('FACTURAENLINEA', 'facturaenlinea.cl'),
            ('LIBREDTE', 'LibreDTE'),
            ('LIBREDTE_TEST', 'LibreDTE (test mode)'),
            ('SIIHOMO', 'SII - Certification process'),
            ('SII', 'www.sii.cl'),
            ('SII MiPyme', 'SII - Portal MiPyme'),
        ), 'DTE Service Provider',
        related='company_id.dte_service_provider',
        #default=get_company_dte_service_provider,
        readonly=True)

    # estas referencias existen de la versión anterior (8.0.1.3)
    # ToDO: quitarlas para que se reemplacen totalmente por campos
    # referenciales
    '''
    a partir del cambio, estos campos quedarían obsoletos.
    Los dejamos, para mantener compatibilidad de información
    en instalaciones previas, y que no haya posibilidad de perdida
    de datos ante un cleanup de la bdd.
    --------------------------------------------------------------
    '''
    sii_referencia_TpoDocRef = fields.Char('TpoDocRef')
    sii_referencia_FolioRef =  fields.Char('FolioRef')
    sii_referencia_FchRef = fields.Char('FchRef')
    sii_referencia_CodRef = fields.Char('CodRef')

    # campos nuevos para incluir referencias relacionales
    # (para no tener un limiteen la cantidad de referencias al documento)
    # ver la nueva clase que se agrega (referencias)
    ref_document_ids = fields.One2many(
        'invoice.reference', 'invoice_id', string='Document References')

    dte_resolution_number = fields.Char('SII Exempt Resolution Number',
                                        help='''This value must be provided \
and must appear in your pdf or printed tribute document, under the electronic \
stamp to be legally valid.''')

    # third_party_xml = fields.Binary('XML File', copy=False)
    filename_xml = fields.Char('File Name XML')

    @api.multi
    def get_related_invoices_data(self):
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
    def bring_xml_ldte(self, response_emitir_data):
        """
        Función para tomar el XML generado en libreDTE y adjuntarlo al registro
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-23
        """
        self.ensure_one()
        _logger.info('entrada a bringxml function')
        headers = self.create_headers_ldte()
        response_generar = pool.urlopen(
            'POST', api_generar, headers=headers,
            body=response_emitir_data)
        if response_generar.status != 200:
            raise UserError('Error en conexión al generar: %s, %s' % (
                response_generar.status, response_generar.data))
        _logger.info('response_generar: %s' % response_generar.data)
        self.sii_xml_response1 = response_emitir_data
        try:
            response_j = json.loads(response_generar.data)
        except:
            raise UserError('LibreDTE No pudo generar el XML.\n'
                'Reintente en un instante. \n{}'.format(
                response_generar.data))
        _logger.info(response_j)
        '''
        {"emisor":76085472,"dte":56,"folio":3,"certificacion":1,"tasa":19,
        "fecha":"2016-07-02","sucursal_sii":null,"receptor":"00000001",
        "exento":null,"neto":230000,"iva":43700,"total":273700,"usuario":1639,
        {'emisor', 'dte', 'folio', 'certificacion', 'tasa', 'fecha',
         'sucursal_sii', 'receptor', 'exento', 'neto', 'iva', 'total',
         'usuario'}'''

        attachment_obj = self.env['ir.attachment']
        _logger.info('Attachment')
        _logger.info(self.sii_document_class_id.name)
        _logger.info(response_j['folio'])
        attachment_id = attachment_obj.create(
            {
                'name': 'DTE_'+self.sii_document_class_id.name+'-'+str(
                    response_j['folio'])+'.xml',
                'datas': response_j['xml'],
                'datas_fname': 'DTE_'+self.sii_document_class_id.name+'-'+str(
                    response_j['folio'])+'.xml',
                'res_model': self._name,
                'res_id': self.id,
                'type': 'binary'
            })
        _logger.info('Se ha generado factura en XML con el id {}'.format(
            attachment_id))
        return response_j

    @api.multi
    def get_xml_attachment(self):
        """
        Función para leer el xml para libreDTE desde los attachments
        @author: Daniel Blanco Martín (daniel[at]blancomartin.cl)
        @version: 2016-07-01
        """
        self.ensure_one()
        _logger.info('entrando a la funcion de toma de xml desde attachments')
        pass
        attachment_id = self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id,),
            ('name', 'like', 'DTE_'),
            ('name', 'ilike', '.xml')])

        for att_id in attachment_id:
            _logger.info(att_id.id)
            xml_attachment = att_id.datas
            break
        return xml_attachment

    '''
    A partir de aca se realiza la toma del pdf con la factura impresa
    directamente desde libreDTE
    podria existir la posibilidad técnica de imprimir la factura
    desde odoo con otro módulo l10n_cl_dte_pdf
    o desde esta "función"
    obtener el PDF desde LibreDTE
    '''
    @api.multi
    def bring_pdf_ldte(self):
        """
        Función para tomar el PDF generado en libreDTE y adjuntarlo al registro
        @author: Daniel Blanco Martin (daniel[at]blancomartin.cl)
        @version: 2016-06-23
        Se corrige función para que no cree un nuevo PDF cada vez que se hace clic en botón
        y no tome PDF con cedible que se creará en botón imprimir.
        @review: Juan Plaza (jplaza@isos.cl)
        @version: 2016-09-28
        """
        attachment_obj = self.env['ir.attachment']
        if attachment_obj.search(
                [('res_model', '=', self._name), ('res_id', '=', self.id,),
                 ('name', 'like', 'DTE_'),
                 ('name', 'not like', 'cedible'), ('name', 'ilike', '.pdf')]):
            pass
        else:
            self.ensure_one()
            _logger.info('entrada a bringpdf function')
            headers = self.create_headers_ldte()
            # en lugar de third_party_xml, que ahora no va a existir más,
            # hay que tomar el xml del adjunto, o bien del texto
            # pero prefiero del adjunto
            dte_xml = self.get_xml_attachment()
            generar_pdf_request = json.dumps(
                {'xml': dte_xml, 'compress': False})
            _logger.info(generar_pdf_request)
            response_pdf = pool.urlopen(
                'POST', api_gen_pdf, headers=headers,
                body=generar_pdf_request)
            if response_pdf.status != 200:
                raise Warning('Error en conexión al generar: %s, %s' % (
                    response_pdf.status, response_pdf.data))
            invoice_pdf = base64.b64encode(response_pdf.data)
            attachment_obj = self.env['ir.attachment']
            attachment_id = attachment_obj.create(
                {
                    'name': 'DTE_' + self.sii_document_class_id.name + '-' + self.sii_document_number + '.pdf',
                    'datas': invoice_pdf,
                    'datas_fname': 'DTE_' + self.sii_document_class_id.name + '-' + self.sii_document_number + '.pdf',
                    'res_model': self._name,
                    'res_id': self.id,
                    'type': 'binary'})
            _logger.info('Se ha generado factura en PDF con el id {}'.format(
                attachment_id))


    def product_is_exempt(self, line):
        """
        Función para determinar si el producto de la linea corriente es exento
        :param line:
        :return:
        """
        return line.product_id.is_exempt

    @api.multi
    def action_invoice_sent(self):
        """
        Funcion que envía el email por correo electrónico al cliente
        es la funcion original en la cual se ha modificado la plantilla
        para que en lugar de enviar un reporte envíe los attachment que cumplan
        la condición deseada. (empiezan con DTE_)
        autor de la modificacion: Daniel Blanco - daniel[at]blancomartin.cl
        @version: 2016-06-27
        Open a window sentto compose an email, with the edi invoice template
        message loaded by default
        """
        _logger.info('controlo el proceso de envio con mi propia funcion...')
        if len(self) != 1:
            raise UserError('This option should only be used for a single id \
at a time.')
        attachment_id = self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id,),
            ('name', 'like', 'DTE_')])

        atts_ids = []
        for att_id in attachment_id:
            _logger.info(att_id.id)
            atts_ids.append(att_id.id)
        _logger.info(atts_ids)

        ## hace este cambio: reemplaza el template (inicio)
        template = self.env.ref('l10n_cl_dte.email_template_edi_invoice', False)
        ## hace este cambio: reemplaza el template (fin)
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            default_attachment_ids=atts_ids,
            mark_invoice_as_sent=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
    '''
    Funcion que reemplaza función de botón imprimir para generar PDF
    con cedible, función solo para LibreDTE.
    TODO: poner comprobación de existencia de PDF al principio
    autor: Juan Plaza - jplaza@isos.cl basado en función de Daniel Blanco
    @version: 2016-09-28
    '''
    @api.multi
    def invoice_print(self):
        _logger.info('entrando a impresion de factura desde boton de arriba')
        self.ensure_one()
        _logger.info('entrada a invoice print function')
        headers = self.create_headers_ldte()
        # en lugar de third_party_xml, que ahora no va a existir más,
        # hay que tomar el xml del adjunto, o bien del texto
        # pero prefiero del adjunto
        dte_xml = self.get_xml_attachment()
        genera_pdf_request = json.dumps(
            {'xml': dte_xml, 'cedible': 1, 'copias_tributarias': 1, 'copias_cedibles': 1, 'compress': False})
        _logger.info(genera_pdf_request)
        response_pdf = pool.urlopen(
            'POST', api_gen_pdf, headers=headers,
            body=genera_pdf_request)
        if response_pdf.status != 200:
            raise Warning('Error en conexión al bkgenerar: %s, %s' % (
                response_pdf.status, response_pdf.data))
        invoice_pdf = base64.b64encode(response_pdf.data)
        # assert len(self) == 1, self.sent = True
        # return self.env['report'].get_action(self, 'account.report_invoice')
        attachment_obj = self.env['ir.attachment']
        if attachment_obj.search([('res_model', '=', self._name), ('res_id', '=', self.id,), ('name', 'like', 'cedible')]):
            new_attach = attachment_obj.search(
                [('res_model', '=', self._name), ('res_id', '=', self.id,), ('name', 'like', 'cedible')])

        else:
            new_attach = attachment_obj.create(
                {
                    'name': 'DTE_' + self.sii_document_class_id.name + '-' + self.sii_document_number + 'cedible.pdf',
                    'datas': invoice_pdf,
                    'datas_fname': 'DTE_' + self.sii_document_class_id.name + '-' + self.sii_document_number + 'cedible.pdf',
                    'res_model': self._name,
                    'res_id': self.id,
                    'type': 'binary'
                })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id=%s' % (new_attach.id,),
            'target': 'self',
        }

    @api.multi
    def action_number(self):
        self.do_dte_send_invoice()
        res = super(invoice, self).action_number()
        return res

    @api.multi
    def do_dte_send_invoice(self):
        cant_doc_batch = 0
        for inv in self.with_context(lang='es_CL'):
            if inv.type[:2] == 'in':
                continue
            # control de DTE
            if inv.sii_document_class_id.dte == False:
                continue
            # control de DTE
            cant_doc_batch = cant_doc_batch + 1

            if inv.dte_service_provider in ['EFACTURADELSUR',
                                            'EFACTURADELSUR_TEST',
                                            'LIBREDTE',
                                            'LIBREDTE_TEST']:
                # debe utilizar usuario y contraseña
                # todo: hardcodeado, pero pasar a webservices server
                dte_username = self.company_id.dte_username
                dte_password = self.company_id.dte_password

            elif inv.dte_service_provider in ['', 'NONE']:
                return

            # definicion de los giros del emisor
            giros_emisor = []
            for turn in inv.company_id.company_activities_ids:
                giros_emisor.extend([{'Acteco': turn.code}])
            # definicion de lineas
            line_number = 1
            invoice_lines = []
            global_discount = 0
            ind_exe_qty = 0
            sum_lines = 0
            MntExe = 0
            for line in inv.invoice_line:
                # se hizo de esta manera para que no dé error
                try:
                    if line.product_id.is_discount:
                        # es un producto usado para representar descuentoe
                        global_discount += int(round(line.price_subtotal, 0))
                        continue
                except:
                    if u'descuento' in line.product_id.name.lower():
                        global_discount += int(round(line.price_subtotal, 0))
                        continue
                    else:# no existe el campo is_discount
                        pass
                sum_lines += line.price_subtotal
                lines = collections.OrderedDict()
                lines['NroLinDet'] = line_number
                if line.product_id.default_code:
                    lines['CdgItem'] = collections.OrderedDict()
                    lines['CdgItem']['TpoCodigo'] = 'INT1'
                    lines['CdgItem']['VlrCodigo'] = line.product_id.default_code
                # todo: mejorar el cálculo de impuestos

                if self.product_is_exempt(line):
                    # manejo de error: momentaneamente para simplificar los
                    # cálculos de impuestos, se impide colocar items exentos
                    # en una factura afecta
                    if inv.sii_document_class_id.sii_code == 33:
                        raise UserError('''Esta implementación no permite \
facturar items exentos en facturas afectas. Cambie el tipo de documento \
o elimine el producto exento de esta factura.
Producto que provocó el problema: {}'''.format(line.product_id.name))
                    lines['IndExe'] = 1
                    ind_exe_qty += 1
                    MntExe +=int(round(line.price_subtotal, 0))

                lines['NmbItem'] = self.char_replace(line.product_id.name)[:80]
                lines['DscItem'] = line.name
                # si es cero y es nota de crédito o debito, los salteo a los dos
                if line.quantity == 0 and line.price_unit == 0 and \
                                inv.sii_document_class_id.sii_code in [61, 56]:
                    pass
                else:
                    lines['QtyItem'] = round(line.quantity, 4)
                    # todo: opcional lines['UnmdItem'] = line.uos_id.name[:4]
                    # reemplazo la formula de precio unitario para que sea
                    # independiente de si se incluye o no el iva en el precio
                    # lines['PrcItem'] = round(line.price_unit, 4)
                    price_unit = (line.price_subtotal/line.quantity) / (
                        1-line.discount/100)
                    lines['PrcItem'] = round(price_unit, 4)

                if 1==1:
                    # try:
                    if line.discount != 0:
                        lines['DescuentoPct'] = round(line.discount, 2)
                        lines['DescuentoMonto'] = int(
                            round((line.quantity * price_unit * line.discount) \
                                  / 100, 0))
                else:
                    #except:
                    pass
                lines['MontoItem'] = int(round(line.price_subtotal, 0))
                line_number = line_number + 1
                if inv.dte_service_provider not in [
                    'LIBREDTE', 'LIBREDTE_TEST']:
                    invoice_lines.extend([{'Detalle': lines}])
                else:
                    invoice_lines.extend([lines])
            if len(invoice_lines) == ind_exe_qty \
                    and inv.sii_document_class_id.sii_code not in [34, 61]:
                raise UserError(_('All items are VAT exempt. Type of document \
is {} does not match'.format(inv.sii_document_class_id.sii_code)))
            ref_lines = []
            if len(inv.ref_document_ids) > 0:
                _logger.info(inv.ref_document_ids)
                # inserción del detalle en caso que corresponda
                #if inv.sii_document_class_id.sii_code in [61, 56]:
                ref_order = 1
                for ref_d in inv.ref_document_ids:
                    referencias = collections.OrderedDict()
                    referencias['NroLinRef'] = ref_order
                    referencias[
                        'TpoDocRef'] = ref_d.prefix
                    referencias['FolioRef'] = ref_d.name
                    referencias['FchRef'] = ref_d.reference_date
                    if ref_d.codref:
                        referencias['CodRef'] = ref_d.codref
                    if ref_d.reason:
                        referencias['RazonRef'] = ref_d.reason
                    ref_order += 1
                    if inv.dte_service_provider not in [
                        'LIBREDTE', 'LIBREDTE_TEST']:
                        ref_lines.extend([{'Referencia': referencias}])
                    else:
                        ref_lines.extend([referencias])

            ##### lugar de corte posible para revisar creacion de test:
            # _logger.info(invoice_lines)
            #########################

            folio = self.get_folio(inv)
            dte = collections.OrderedDict()
            dte1 = collections.OrderedDict()

            # dte['Documento ID'] = 'F{}T{}'.format(
            # folio, inv.sii_document_class_id.sii_code)
            dte['Encabezado'] = collections.OrderedDict()
            dte['Encabezado']['IdDoc'] = collections.OrderedDict()
            dte['Encabezado']['IdDoc'][
                'TipoDTE'] = inv.sii_document_class_id.sii_code
            dte['Encabezado']['IdDoc']['Folio'] = folio
            if inv.dte_service_provider not in ['LIBREDTE', 'LIBREDTE_TEST']:
                dte['Encabezado']['IdDoc']['FchEmis'] = inv.date_invoice
            # todo: forma de pago y fecha de vencimiento - opcional
            dte['Encabezado']['IdDoc'][
                'FmaPago'] = inv.payment_term.dte_sii_code or 1
            if inv.date_due < inv.date_invoice:
                raise UserError('LA FECHA DE VENCIMIENTO'\
'NO PUEDE SER ANTERIOR A LA DE FACTURACION: Fecha de Facturación: {}, Fecha \
de Vencimiento {}'.format(inv.date_invoice, inv.date_due))
            dte['Encabezado']['IdDoc']['FchVenc'] = inv.date_due
            dte['Encabezado']['Emisor'] = collections.OrderedDict()
            dte['Encabezado']['Emisor']['RUTEmisor'] = self.format_vat(
                inv.company_id.vat)
            dte['Encabezado']['Emisor']['RznSoc'] = inv.company_id.name
            dte['Encabezado']['Emisor']['GiroEmis'] = self.char_replace(
                inv.turn_issuer.name)[:80]
            if inv.dte_service_provider not in ['LIBREDTE', 'LIBREDTE_TEST']:
                dte['Encabezado']['Emisor']['item'] = giros_emisor
                # giros de la compañia - codigos
            else:
                dte['Encabezado']['Emisor']['Acteco'] = inv.turn_issuer.code
                # dte['Encabezado']['Emisor']['Acteco'] = giros_emisor
                #  giros de la compañia - codigos
            # todo: Telefono y Correo opcional
            dte['Encabezado']['Emisor']['Telefono'] = inv.company_id.phone or ''
            dte['Encabezado']['Emisor'][
                'CorreoEmisor'] = inv.company_id.dte_email
            # dte['Encabezado']['Emisor']['item'] = giros_emisor
            #  giros de la compañia - codigos
            # todo: <CdgSIISucur>077063816</CdgSIISucur> codigo de sucursal
            # no obligatorio si no hay sucursal, pero es un numero entregado
            # por el SII para cada sucursal.
            # este deberia agregarse al "punto de venta" el cual ya esta
            dte['Encabezado']['Emisor']['DirOrigen'] = self.char_replace(
                inv.company_id.street)
            dte['Encabezado']['Emisor']['CmnaOrigen'] = self.char_replace(
                inv.company_id.state_id.name)
            dte['Encabezado']['Emisor']['CiudadOrigen'] = self.char_replace(
                inv.company_id.city)
            dte['Encabezado']['Receptor'] = collections.OrderedDict()
            # agregado de posibilidad de multiples direcciones, para el mismo
            # partner si el registro es "hijo de" un partner principal,
            # toma el nombre del partner principal.
            # pero toma la direccion del partner seleccionado.
            if not inv.partner_id.parent_id:
                # si viene por aca quiere decir que estoy tratando con la
                # compañia principal
                dte['Encabezado']['Receptor']['RUTRecep'] = self.format_vat(
                    inv.partner_id.vat)
                dte['Encabezado']['Receptor'][
                    'RznSocRecep'] = inv.partner_id.name
            else:
                # si viene por aca significa que estoy en un partner "hijo"
                # y debo tomar la razon social principal
                dte['Encabezado']['Receptor']['RUTRecep'] = self.format_vat(
                    inv.partner_id.parent_id.vat)
                dte['Encabezado']['Receptor'][
                    'RznSocRecep'] = inv.partner_id.parent_id.name
            if not inv.invoice_turn.name:
                raise UserError(_('There is no customer turn selected.'))
            dte['Encabezado']['Receptor']['GiroRecep'] = self.char_replace(
                inv.invoice_turn.name)[:40]
            dte['Encabezado']['Receptor']['DirRecep'] = self.char_replace(
                inv.partner_id.street)
            # todo: revisar comuna: "false"
            if inv.partner_id.state_id.name == False or \
                            inv.partner_id.city == False:
                raise UserError(
                    'No se puede continuar: Revisar comuna y ciudad')
            dte['Encabezado']['Receptor']['CmnaRecep'] = self.char_replace(
                inv.partner_id.state_id.name)
            dte['Encabezado']['Receptor']['CiudadRecep'] = self.char_replace(
                inv.partner_id.city)
            #################################################
            if inv.dte_service_provider not in ['LIBREDTE', 'LIBREDTE_TEST']:
                # no se envían los totales a LibreDTE
                dte['Encabezado']['Totales'] = collections.OrderedDict()
                if inv.sii_document_class_id.sii_code == 34:
                    # en el caso que haya un tipo 34, el monto
                    # exento va a coincidir con el total de la factura.
                    dte['Encabezado']['Totales']['MntExe'] = int(round(
                        inv.amount_total, 0))
                else:
                    # acá puede ocurrir que haya valores exentos involucrados
                    dte['Encabezado']['Totales']['MntNeto'] = int(round(
                        inv.amount_untaxed, 0))
                    try:
                        dte['Encabezado']['Totales']['TasaIVA'] = int(round(
                            (inv.amount_total / inv.amount_untaxed - 1) * 100,
                            0))
                        # TODO: si este valor es distinto a 19%, hay un error
                        # salvo que haya retenciones, que eso queda por hacer
                    except:
                        # lo hardcodeamos para solucionar rapidamente el
                        # problema cuando se usan n/c o n/d para hacer
                        # modificaciones
                        _logger.info('calculo de iva total por excepcion')
                        dte['Encabezado']['Totales']['TasaIVA'] = 19
                    MntTotal = int(round(inv.amount_total, 0))
                    dte['Encabezado']['Totales']['IVA'] = MntTotal - dte[
                        'Encabezado']['Totales']['MntNeto']
                    dte['Encabezado']['Totales']['MntTotal'] = MntTotal
                dte['item'] = invoice_lines
                if len(ref_lines) > 0:
                    dte['item'].extend(ref_lines)
            else:
                # esto lo hace para libreDTE la construccion directa del valor
                # en el diccionario. Porque en las otras opciones de XML
                # hay problemas en esta parte al pasar de dict a xml
                dte['Detalle'] = invoice_lines
                if len(ref_lines) > 0:
                    dte['Referencia'] = ref_lines
            # aca estaba la referencia antes
            if global_discount != 0:
                dte['DscRcgGlobal'] = collections.OrderedDict()
                dte['DscRcgGlobal']['NroLinDR'] = 1
                dte['DscRcgGlobal'][
                    'TpoMov'] = 'D' if global_discount < 0 else 'R'
                dte['DscRcgGlobal']['TpoValor'] = '$'  # ''%'
                dte['DscRcgGlobal']['ValorDR'] = round(abs(global_discount))
            _logger.info(dte)
            doc_id_number = "F{}T{}".format(
                folio, inv.sii_document_class_id.sii_code)
            doc_id = '<Documento ID="{}">'.format(doc_id_number)
            # TODO: si es sii, inserto el timbre

            dte1['Documento ID'] = dte
            xml = dicttoxml.dicttoxml(
                dte1, root=False, attr_type=False).replace(
                    '<item>','').replace('</item>','')

            root = etree.XML( xml )

            xml_pret = etree.tostring(root, pretty_print=True).replace(
'<Documento_ID>', doc_id).replace('</Documento_ID>', '</Documento>')

            xml_pret = self.create_template_doc(xml_pret)

            if inv.dte_service_provider in [
                'EFACTURADELSUR', 'EFACTURADELSUR_TEST']:
                enviar = 'true' if self.dte_service_provider == \
                                   'EFACTURADELSUR' else 'false'
                # armado del envolvente rrespondiente a EACTURADELSUR
                envelope_efact = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
<soap12:Body>
<PonerDTE xmlns="https://www.efacturadelsur.cl">
<usuario>{0}</usuario>
<contrasena>{1}</contrasena>
<xml><![CDATA[{2}]]></xml>
<enviar>{3}</enviar>
</PonerDTE>
</soap12:Body>
</soap12:Envelope>'''.format(dte_username, dte_password, xml_pret, enviar)
                _logger.info(inv.sii_xml_request)
                inv.sii_xml_request = envelope_efact
                inv.sii_result = 'NoEnviado'
                _logger.info('OPCION DTE: ({})'.format(str(
                    inv.dte_service_provider)).lower())
            elif inv.dte_service_provider in [
                'LIBREDTE', 'LIBREDTE_TEST']:
                _logger.info('password: %s' % self.company_id.dte_password)
                _logger.info('username: %s' % self.company_id.dte_username)

                headers = self.create_headers_ldte()
                _logger.info('Headers:')
                _logger.info(headers)
                _logger.info('DTE enviado:')
                _logger.info(dte)
                _logger.info('DTE enviado (json)')
                _logger.info(json.dumps(dte))

                # corte para debug
                # raise UserError('dictionary generated')
                # if inv.sii_xml_response1 == False or \
                # inv.sii_xml_response1 == '':
                # buscar una manera de forzar el reenvio.
                # por ahora fuerza el reenvío desde el principio
                if 1==1:
                    response_emitir = pool.urlopen(
                        'POST', api_emitir, headers=headers, body=json.dumps(
                            dte))

                    if response_emitir.status != 200:
                        raise UserError(
                            'Error en conexión al emitir: {}, {}'.format(
                                response_emitir.status, response_emitir.data))
                    _logger.info('response_emitir: {}'.format(
                        response_emitir.data))
                    try:
                        inv.sii_xml_response1 = response_emitir.data
                    except:
                        _logger.warning(
                            'no pudo guardar la respuesta al ws de emision')
                    '''
                    {"emisor": ----, "receptor": -, "dte": --,
                     "codigo": "-----"}
                    '''
                    response_emitir_data = response_emitir.data
                else:
                    _logger.info('Obteniendo XML de preemision existente...')
                    response_emitir_data = inv.sii_xml_response1

                response_j = self.bring_xml_ldte(response_emitir_data)
                self.set_folio(inv, response_j['folio'])
                _logger.info('Este es el XML decodificado:')
                _logger.info(base64.b64decode(response_j['xml']))

                try:
                    inv.sii_xml_request = self.convert_encoding(
                        base64.b64decode(response_j['xml']))
                except:
                    pass
                    _logger.warning(
                        'no pudo codificar y guardar el documento... ')

                try:
                    self.bring_pdf_ldte()
                except:
                    pass
                    _logger.warning('no pudo traer el pdf')

                inv.write(
                    {
                        #'third_party_xml': response_j['xml'],
                        'sii_result': 'Enviado',
                        'sii_send_ident': response_j['track_id'],
                        # 'third_party_pdf': base64.b64encode(invoice_pdf)
                    }
                )
                _logger.info('se guardó xml con la factura')
            # incorporo facturacion.cl (sólo DTE Plano)
            elif inv.dte_service_provider == 'FACTURACION':
                envelope_efact = '''<?xml version="1.0" encoding="ISO-8859-1"?>
{}'''.format(self.convert_encoding(xml_pret, 'ISO-8859-1'))
                inv.sii_xml_request = envelope_efact
                # raise UserError(envelope_efact)
                # self.get_xml_file()
            else:
                _logger.info('NO HUBO NINGUNA OPCION DTE VALIDA ({})'.format(
                    inv.dte_service_provider))
                raise UserError('None DTE Provider Option')


class invoiceReference(models.Model):
    _name = "invoice.reference"
    '''
    C<NroLinRef> ordinal. No se incluye. Se debe calcular al crear el
    diccionario
    C<TpoDocRef> i.sii_document_class_id.sii_code
    *<FolioRef>  name
    *<FchRef>	reference_date
    *<CodRef>    codref
    *<RazonRef>  reason
    N<RUTOtr>    no implementado (por ahora)
    N<IdAdicOtr> no implementado (por ahora)
    N<IndGlobal> no se incluye
    '''

    # Esta Factura
    invoice_id = fields.Many2one(
        'account.invoice', 'Invoice',
        required=True, ondelete='cascade', select=True, readonly=True)
    # FolioRef
    name = fields.Char(
        'Number', required=True, readonly=False,
        help='Number (folio) of reference')
    sii_document_class_id = fields.Many2one(
        'sii.document_class', 'Ref Document',
        required=True, ondelete='cascade')
    # FchRef
    reference_date = fields.Date(
        'Ref. Date', required=True, help="FchRef")
    # si no hay un document class, puede tomar de éste (no implementado)
    # por ejemplo "SET" para set de pruebas <TipoDocRef>
    # si existe un sii_code toma el sii code. si no existe, lo tiene que tomar
    # desde acá. (la idea es que todos los posibles existan en el modelo
    # sii.document_class)
    prefix = fields.Char(
        'Prefix', compute='_compute_ref' ,readonly=True,
        help="<TipoDocRef>. Should be SII Code for docs, or this prefix if \
does not exist.")
    # CodRef.. se usa solo si el doc principal es nota de credito o débito
    codref = fields.Char('Cod.Ref', readonly=True, help="<CodRef>, Only \
needed for credit notes and debit notes.")
    # RazonRef "descuento por pronto pago" o "error en precio"
    reason = fields.Char('Reason', help="Related to <RazonRef>.")

    #doc_princ_sii_code = fields.Integer('Documento Principal', compute='')


    @api.multi
    @api.depends('sii_document_class_id')
    def _compute_ref(self):
        for i in self:
            if not i.sii_document_class_id.sii_code \
                    and i.sii_document_class_id.doc_code_prefix:
                _logger.info(
                'pasa por la funcion compute_ref: {}|{}|{}'.format(
                    i.id, i.name, i.sii_document_class_id.doc_code_prefix))
                i.prefix = i.sii_document_class_id.doc_code_prefix[:3]
            else:
                i.prefix = i.sii_document_class_id.sii_code
