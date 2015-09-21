# -*- coding: utf-8 -*-
from openerp.osv import osv
import urllib2 as u

import simplejson as json


class l10n_cl_financial_indicators(osv.osv):
    _name = "res.currency.rate"
    _inherit = "res.currency.rate"

    # schedule update
    def currency_schedule_update(self, cr, uid, context=None):
        from apikey import apikey
        indicadores = {
            ('dolar', 'Dolares', 'USD'),
            ('euro', 'Euros', 'EUR'),
            ('uf', 'UFs', 'UF'),
            ('utm', 'UTMs', 'UTM'),
        }

        for indic in indicadores:
            url = 'http://api.sbif.cl/api-sbifv3/recursos_api/'+indic[0]
            url += '?apikey='+apikey+'&formato=json'
            f = u.urlopen(url)
            data = f.read()
            data_json = json.loads(data)
            rate = data_json[indic[1]][0]['Valor'].replace('.', '')
            rate = float(rate.replace(',', '.'))
            currency_obj = self.pool.get('res.currency')
            currency_rate_obj = self.pool.get('res.currency.rate')
            currency_id = currency_obj.search(cr, uid, [(
                'name', '=', indic[2])])
            #print "Actualizacion " + indic[2]
            if not currency_id:
                print "No esta cargado el " + indic[2]
            else:
                print "Actualizando " + indic[2]
                values = {
                    'rate': 1/rate,
                    'currency_id': currency_id[0],
                    'currency_type_id': ''
                    }
                currency_rate_obj.create(cr,uid,values)

        return True
    
l10n_cl_financial_indicators()
