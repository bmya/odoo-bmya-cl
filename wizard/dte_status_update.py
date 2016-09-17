# -*- coding: utf-8 -*-
from __future__ import print_function
from openerp import fields, models, api
from openerp.tools.translate import _
import logging
import collections
from openerp.exceptions import Warning


_logger = logging.getLogger(__name__)

class accountInvoiceDTEStatus(models.TransientModel):

    _name = 'account.invoice.dte_status'

    def _get_default_sii_result(self):
        '''
        Función para poner en default el valor de sii_result
        de manera que venga desde el proceso que llama
        (lo toma desde el contexto)
        @author: Daniel Blanco Martín daniel[at]blancomartin.cl
        @version: 2016-06-18
        contexto de ejemplo, para cualquier otro valor de intercambio que
        haga falta:
        {
            'lang': 'es_CL',
            'tz': 'America/Santiago',
            'uid': 1,
            'active_model': 'account.invoice',
            'journal_type': 'sale',
            'sii_status': 'NoEnviado',
            'params':
                {
                    'action': 255,
                    'model': 'account.invoice',
                     '_push_me': False,
                     'id': 241,
                     'view_type': 'form'
                },
            'dte_service_provider': 'EFACTURADELSUR_TEST',
            'search_disable_custom_filters': True,
            'active_ids': [245],
            'type': 'out_invoice',
            'active_id': 245
        }
        '''
        return self.env.context['sii_status']

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
        help="SII request result",
        default=_get_default_sii_result)

    sii_send_ident = fields.Char(
        string='SII Send Identification')

    glosa = fields.Text(
        string='Glosa')

    @api.multi
    @api.depends('sii_result', 'sii_send_ident', 'glosa')
    def update_dte_status(self):
        '''
        Función para ejecutar el cambio de estado del DTE
        @author: Daniel Blanco Martín daniel[at]blancomartin.cl
        @version: 2016-06-18
            posibles estados:
            Anulado
            NoEnviado
            Enviado
            Proceso
            Aceptado
            Reparo
            Rechazado
            Reenviar
        '''
        self.ensure_one()
        _logger.info('entrando en funcion update_dte_status')
        # self.env.context.get('value_key', value_if_undefined)
        if self.env.context.get('dte_service_provider') in [
            'EFACTURADELSUR', 'EFACTURADELSUR_TEST']:
            _logger.info('update dte status con facturadelsur')
            # reobtener el folio
            folio = l10n_cl_dte.invoice.get_folio_current()
            dte_username = self.company_id.dte_username
            dte_password = self.company_id.dte_password
            envio_check = '''<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <ActualizarEstadoDTE xmlns="https://www.efacturadelsur.cl">
      <usuario>{0}</usuario>
      <contrasena>{1}</contrasena>
      <rutEmisor>{2}</rutEmisor>
      <tipoDte>{3}</tipoDte>
      <folio>{4}</folio>
      <estado>{5}</estado>
      <glosa>{6}</glosa>
      <idSii>{7}</idSii>
      <fechaEstado>{8}</fechaEstado>
    </ActualizarEstadoDTE>
  </soap12:Body>
</soap12:Envelope>'''.format(
            dte_username,
            dte_password,
            self.format_vat(self.company_id.vat),
            self.sii_document_class_id.sii_code,
            folio,
            estado_nuevo,
            glosa,
            sii_send_ident)

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
                raise Warning(
                    'The Transmission Has Failed. Error: %s' % response.status)

            setenvio = {
                # 'sii_result': 'Enviado' if self.dte_service_provider == 'EFACTURADELSUR' else self.sii_result,
                'sii_xml_response': response.data}
            self.write(setenvio)
            x = xmltodict.parse(response.data)
            raise Warning(x['soap:Envelope']['soap:Body'][
                              'ObtenerEstadoDTEResponse'][
                              'ObtenerEstadoDTEResult'])

            root = etree.fromstring(response.data)
            raise Warning(root.ObtenerEstadoDTEResult)
        elif self.env.context.get('dte_service_provider') in [
            'LIBREDTE', 'LIBREDTE_TEST']:
            print('update dte status con facturadelsur')
            pass

class AccountInvoiceRefund(models.TransientModel):
    '''
    Clase que sirve para redefinir botón de devolucion con notas de
    credito(/debito), para adaptar a los motivos estándares del SII
    @autor: Daniel Blanco Martín
    @version: 2016-07-07
    '''
    _inherit = "account.invoice.refund"

    def get_folio_current(self, inv):
        prefix = inv.journal_document_class_id.sequence_id.prefix
        try:
            folio = inv.sii_document_number.replace(prefix, '', 1)
        except:
            folio = inv.sii_document_number
        return int(folio)

    # definición de campos adicionales.
    # fijar el valor de filter_refund al valor 'refund' por defecto, porque es
    # el único que se utiliza.
    filter_refund = fields.Selection([
        ('refund', 'Create a draft refund'),
        ('cancel', 'Cancel: create refund and reconcile'),
        ('modify', 'Modify: create refund, reconcile and create a new draft \
invoice')], "Refund Method", required=True, help='Refund base on this type. \
You can not Modify an    d Cancel if the invoice is already reconciled',
        default='refund', readonly=True)

    sii_selection = fields.Selection([
        ('1', '1. Anula Documento de Referencia'),
        ('2', '2. Corrige Texto Documento de Referencia'),
        ('3', '3. Corrige Montos (descuentos por ejemplo)')],
        "Tipos de Referencia", required=True, help='Tipos de Referencia',
        default='1')

    @api.multi
    def compute_refund(self, mode='refund'):
        '''
        funcion para grabar en factura original los valores que provienen
        de este wizard.
        @autor: Daniel Blanco Martín
        @version: 2016-07-07
        '''
        self.ensure_one()
        result = super(AccountInvoiceRefund, self).compute_refund(mode)
        inv_obj = self.env['account.invoice']
        ref_obj = self.env['invoice.reference']
        # references = []
        # num = 1
        for active_id in inv_obj.browse(self.env.context.get('active_ids')):
            break
            # references.append(dictos)

        created_inv = [x[2] for x in result['domain']
                       if x[0] == 'id' and x[1] == 'in']

        if created_inv and created_inv[0]:
            refund_inv_id = created_inv[0][0]
            _logger.info('ientra a la opcion de guardar referencia')
            ref_obj.create(
                {
                    'invoice_id': refund_inv_id,
                    'name': self.get_folio_current(active_id),
                    'sii_document_class_id': active_id.sii_document_class_id.id,
                    'reference_date': active_id.date_invoice,
                    'prefix': active_id.sii_document_class_id.sii_code,
                    'codref': self.sii_selection,
                    'reason': self.description,
                })
            # inv_obj.browse(refund_inv_id).write(
            #     {
            #         'origin': self.description,
            #         'reference': active_id.document_number,
            #         'sii_referencia_FolioRef': self.get_folio_current(active_id),
            #         'sii_referencia_TpoDocRef': active_id.sii_document_class_id.sii_code,
            #         'sii_referencia_FchRef': active_id.date_invoice,
            #         'sii_referencia_CodRef': self.sii_selection
            # })
        return result
