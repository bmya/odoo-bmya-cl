# -*- coding: utf-8 -*-
from __future__ import print_function
from openerp import fields, models, api
from openerp.tools.translate import _
import logging
from openerp.exceptions import Warning


_logger = logging.getLogger(__name__)

class account_invoice_dte_status(models.TransientModel):

    _name = 'account.invoice.dte_status'

    '''
    Función para poner en default el valor de sii_result
    de manera que venga desde el proceso que llama
    @author: Daniel Blanco Martín daniel[at]blancomartin.cl
    @version: 2016-06-18
    '''
    def _get_default_sii_result(self):
        '''
        contexto de ejemplo::
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



    '''
    Función para ejecutar el cambio de estado del DTE
    @author: Daniel Blanco Martín daniel[at]blancomartin.cl
    @version: 2016-06-18
    '''
    '''
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
    @api.multi
    @api.depends('sii_result', 'idsii', 'glosa')
    def update_dte_status(self):
        self.ensure_one()
        print('entrando en funcion update_dte_status')
        # self.env.context.get('value_key', value_if_undefined)
        pass
        """
        if self.env.context.get('dte_service_provider') in [
            'EFACTURADELSUR', 'EFACTURADELSUR_TEST']:
            # reobtener el folio
            folio = self.get_folio_current()
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
                idsii)

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
        """
