# -*- coding: utf-8 -*-
from openerp.osv import osv
import urllib2 as u
import simplejson as json

import logging

_logger = logging.getLogger(__name__)


class l10n_cl_financial_indicators(osv.osv):
    _name = "res.currency.rate"
    _inherit = "res.currency.rate"

    # schedule update
    def currency_schedule_update(self, cr, uid, context=None):
        from l10n_cl_financial_indicators.apikey import apikey
        indicadores = {
            ('dolar', 'Dolares', 'USD'),
            ('euro', 'Euros', 'EUR'),
            ('uf', 'UFs', 'UF'),
            ('utm', 'UTMs', 'UTM'),
        }

        for indic in indicadores:
            baseurl = 'http://api.sbif.cl/api-sbifv3/recursos_api/'
            url = baseurl + indic[0] + '?apikey=' + apikey + '&formato=json'
            f = u.urlopen(url)
            data = f.read()
            data_json = json.loads(data)
            rate = float(
                data_json[indic[1]][0]['Valor'].replace(
                    '.', '').replace(',', '.'))
            currency_obj = self.pool.get('res.currency')
            currency_rate_obj = self.pool.get('res.currency.rate')
            currency_id = currency_obj.search(cr, uid, [(
                'name', '=', indic[2])])
            # print "Actualizacion " + indic[2]
            if not currency_id:
                _logger.warning('No esta cargado el %s' % (indic[2]))
            else:
                _logger.info('Actualizando %s' % (indic[2]))
                values = {
                    'rate': 1/rate,
                    'currency_id': currency_id[0],
                    'currency_type_id': ''
                    }
                currency_rate_obj.create(cr, uid, values)

        return True
