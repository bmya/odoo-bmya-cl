from openerp import fields, models, api, _


class dteEmail(models.Model):
    '''
    Email for DTE stuff
    '''
    _inherit = 'res.company'

    dte_email = fields.Char('DTE Email', related='partner_id.dte_email')
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
        ), 'DTE Service Provider', help='''Please select your company service \
provider for DTE service. Select \'None\' if you use manual invoices, fiscal \
controllers or MiPYME Sii Service. Also take in account that if you select \
\'www.sii.cl\' you will need to provide SII exempt resolution number in order \
to be legally enabled to use the service. If your service provider is not \
listed here, please send us an email to soporte@blancomartin.cl in order to \
add the option.''', default='')
    dte_resolution_number = fields.Char('SII Exempt Resolution Number',
                                        help='''This value must be provided \
and must appear in your pdf or printed tribute document, under the electronic \
stamp to be legally valid.''')
    dte_resolution_date = fields.Date('SII Exempt Resolution Date')
    sii_regional_office_id = fields.Many2one(
        'sii.regional.offices', string='SII Regional Office')

    #@api.onchange('state_id')
    #def _selector_sii(self):
    dte_username = fields.Char('DTE Username', help='''Please enter the value \
issued by the DTE Service provider''')
    dte_password = fields.Char(
        'DTE Password/Token', help='''In LibreDTE case, this value is the \
token. In other cases, the pair username/password is needed.''')

