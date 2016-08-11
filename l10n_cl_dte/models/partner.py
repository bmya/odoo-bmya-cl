# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _
from openerp.exceptions import Warning
import logging, json
try:
    import urllib3
except:
    pass

urllib3.disable_warnings()
'''
pip install --upgrade requests
y
pip install --upgrade urllib3
'''
#import urllib3
#import certifi

pool = urllib3.PoolManager()
'''    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)'''
#pool = urllib3.PoolManager()

_logger = logging.getLogger(__name__)

host = 'https://libredte.cl/api'
api_get_partner_data = host + '/dte/contribuyentes/info/'

tax_resp_category = {u'1': u'res_IVARI',  u'2': u'res_BH'}

class dteEmail(models.Model):
    '''
    Email for DTE stuff
    '''
    _inherit = 'res.partner'

    @api.model
    def _get_partner_turn_id(self, giro_id):
        act_obj = self.env['partner.activities']
        act_record = act_obj.search(
            [('code', '=', giro_id)])
        _logger.info('actividad(es): {}'.format(act_record))
        return act_record
        # raise Warning(act_record.id)

    @api.model
    def _get_partner_location_id(self, comuna_id):
        try:
            return self.env.ref('l10n_cl_counties.CL{}'.format(comuna_id))
        except:
            return False

    dte_email = fields.Char('DTE Email')

    @api.multi
    @api.onchange('document_number')
    def get_data_from_libre_dte(self):
        self.ensure_one()
        if self.document_number == False:
            return
        self.document_type_id = self.env.ref('l10n_cl_invoice.dt_RUT')
        rut = int(self.document_number.replace('.', '').replace('-', '')[:-1])
        if self.company_id.dte_service_provider in [
            'LIBREDTE', 'LIBREDTE_TEST']:
            # web service
            inv = self.env['account.invoice']
            headers = inv.create_headers_ldte(self.company_id)
            response_status = pool.urlopen(
                'GET',
                api_get_partner_data + str(rut), headers=headers)

            if response_status.status != 200:
                raise Warning(
                    'Error al obtener datos del contribuyente: {}'.format(
                        response_status.data))
            partner_values = json.loads(response_status.data)
            _logger.info(partner_values)


            # if response_status_j[
            # 'contribuyente'] != False and self.name == False:
            #     _logger.info('Condicion de nombre')
            '''
            recordmap = [
                ['contribuyente', ''],
                ['rut', ''],
                ['dv', ''],
                ['razon_social', 'name'],
                ['giro', ''],
                ['actividad_economica', 'partner_activities_ids'],
                ['telefono', 'phone'],
                ['email', 'email'],
                ['direccion', 'street'],
                ['comuna', 'state_id'],
                ['usuario', ''],
                ['modificado', ''],
                ['config_ambiente_produccion_fecha', ''],
                ['config_ambiente_produccion_numero', ''],
                ['config_email_intercambio_user', 'dte_email'],
                ['config_extra_representante_rut', ''],
                ['config_extra_contador_rut', ''],
                ['config_extra_web', 'website'],
            ]
            '''

            _logger.info('Datos que se obtienen de LibreDTE: {}'.format(
                response_status.data))

            # estos datos los toma de LibreDTE unicamente si están vacíos
            try:
                self.name = partner_values[
                    'contribuyente'].title() if self.name == False \
                    else self.name
            except:
                pass
            try:
                self.name = partner_values[
                    'razon_social'].title() if self.name == False \
                    else self.name
            except:
                pass
            try:
                self.street = partner_values[
                    'direccion'].title() if self.street == False \
                    else self.street
            except:
                pass
            try:
                self.website = partner_values[
                    'config_extra_web'] if self.website == False \
                    else self.website
            except:
                pass
            try:
                self.email = partner_values[
                    'email'] if self.email == False else self.email
            except:
                pass
            try:
                self.dte_email = partner_values[
                    'config_email_intercambio_user']
            except:
                pass
            try:
                location_id = self._get_partner_location_id(
                    partner_values['comuna'])
                _logger.info('location id: {}'.format(location_id))
                self.country_id = location_id.country_id
                self.state_id = location_id.id
                self.city = location_id.name
            except:
                _logger.warning('could not get location id info from libredte')
            try:
                giro = self._get_partner_turn_id(
                    str(partner_values['actividad_economica']))
                self.partner_activities_ids = [(4, giro.id)]
                _logger.info('Tax category: {}'.format(giro.tax_category))
                if 1==1:
                    self.responsability_id = self.env.ref(
                        'l10n_cl_invoice.{}'.format(tax_resp_category[
                                                        giro.tax_category])).id
                else:
                    _logger.warning(
                        'tax category could not be properly selected')
            except:
                _logger.warning('could not get turn info from libredte')
        else:
            _logger.warning('get_data_from_libre_dte: service provider must\
            be selected properly')
