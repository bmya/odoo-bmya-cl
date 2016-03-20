# -*- coding: utf-8 -*-
from openerp import models, fields, api
#from openerp.osv import fields as old_fields
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
import logging
from openerp.tools.translate import _
import json
import openerp.addons.decimal_precision as dp

indicadores = {
    'SBIFUSD':['dolar', 'Dolares', 'sbif_usd', 'USD'],
    'SBIFEUR':['euro', 'Euros', 'sbif_eur', 'EUR'],
    'SBIFUF':['uf', 'UFs', 'sbif_uf', 'UF'],
    'SBIFUTM':['utm', 'UTMs', 'sbif_utm', 'UTM'],
}

_logger = logging.getLogger(__name__)

class l10n_cl_financial_indicators(models.Model):
    _inherit = "webservices.server"

    @api.multi
    def action_update_currency(self):
        self.ensure_one()
        _logger.info('nombre: %s' % self.name)
        _logger.info('url: %s' % self.url)
        a = self.generic_connection()
        _logger.info('Datos recibidos... status: %s' % a['status'])
        if a['status'] != 200:
            _logger.warning('no se pudo conectar: %s' % a['data'])
            return

        data_json = a['data']
        
        _logger.info('datos mostrados localmente... Fecha: %s, Valor: %s' %
            (data_json[indicadores[self.name][1]][0]['Fecha'],
             data_json[indicadores[self.name][1]][0]['Valor']))
        
        rate = float(
            data_json[indicadores[self.name][1]][0]['Valor'].replace(
                '.', '').replace(',', '.'))

        _logger.info('rate: %s' % str(rate))

        rate_name = fields.Datetime.to_string(datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0))

        currency_id = self.env['res.currency'].search([(
                    'name', '=', indicadores[self.name][3])])

        if not currency_id:
            _logger.warning(
                'No esta cargada "%s" como moneda. No se actualiza.'
                % indicadores[self.name][1])
        else:
            _logger.info(
                'Actualizando la moneda "%s"' % indicadores[self.name][1])
            values = {
                'currency_id': currency_id.id,
                'rate': 1/rate,
                'name': rate_name
                }
            self.env['res.currency.rate'].create(values)
            _logger.info(
                'Se actualizó la moneda "%s".' % indicadores[self.name][1])
    
    '''
    Ejemplo de resultado bueno:
    Result: {u'UFs': [{u'Fecha': u'2016-01-16', u'Valor': u'25.629,09'}]}!
    Ejemplo de resultado malo:
    Result: {"CodigoHTTP": 404, "CodigoError": 81, "Mensaje": "El recurso correspondiente al dia actual aun no ha sido cargado" }!
    '''
 
    def currency_schedule_update(self):
        
        for indic in indicadores.iteritems():

            sbif_svr_data = self.env['webservices.server'].search(
                [('name', '=', indic[0])])

            # print 'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
            # print sbif_svr_data.name
            _logger.info(
                'Iterando la moneda "%s" por proceso planificado'
                % indic[0])

            sbif_svr_data.action_update_currency()

        return True

